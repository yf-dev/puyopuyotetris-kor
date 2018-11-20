import argparse
import glob
from os.path import join as path_join
from os.path import abspath, basename, isfile
from os import makedirs, pardir, remove, listdir, sep, urandom
from subprocess import Popen, PIPE
from tempfile import gettempdir
from shutil import rmtree, copyfile
import re
import sys
from locale import getdefaultlocale
from app.utils.io import print_process
from multiprocessing import Pool
from functools import partial
from uuid import UUID

CONSOLE_ENCODING = getdefaultlocale()[1]

TEMP_DIR_PAR = path_join(gettempdir(), "puyopuyotetris-tempdata")

def mkdir_parent(file_path):
    makedirs(abspath(path_join(file_path, pardir)), exist_ok=True)


def convert_png_to_dds(png_path, imagemagick_convert_path, dds_path=None):
    if dds_path is None:
        dds_path = png_path[: -len(".png")]
    if isfile(dds_path):
        print(f"[-] Remove old dds file {dds_path}...")
        remove(dds_path)
    print(f"[-] Convert png file {png_path} to dds...")
    process = Popen(
        f"{imagemagick_convert_path} -define dds:compression=dxt5 {png_path} {dds_path}",
        stdout=PIPE,
        stderr=PIPE,
    )
    print_process(process, CONSOLE_ENCODING)


def update_fif_data(
    fif_path, base, text_json_file, narc_tmp_path, font, alternative_font, imagemagick_convert_path
):
    index = int(basename(fif_path)[len(f"{base}English_") :][:2], base=10)
    fif_base = fif_path[: -len(".fif.json")]
    font_rel_size = 0
    font_top_margin = 0
    if 'adv_menu' in abspath(fif_path).split(sep)[-1]:
        font_rel_size = -5
        font_top_margin = 4
    if 'staff_roll' in abspath(fif_path).split(sep)[-1]:
        font_rel_size = -9
        font_top_margin = 5
    fif_command = f"python generate_font_data.py {text_json_file} {narc_tmp_path} {fif_base} -f {fif_path} -g {font} -a {alternative_font} -i {index} --font_rel_size {font_rel_size} --font_top_margin {font_top_margin}"
    print(f"[-] Generate fif file and font images from {fif_path}...")
    # print(fif_command)
    process = Popen(fif_command, stdout=PIPE, stderr=PIPE)
    print_process(process, CONSOLE_ENCODING)

    ddss = glob.glob(
        path_join(narc_tmp_path, "**", f"{fif_base}_[0-9][0-9].dds"), recursive=True
    )
    for dds in ddss:
        print(f"[-] Remove old dds file {dds}...")
        remove(dds)

    pngs = glob.glob(
        path_join(narc_tmp_path, "**", f"{fif_base}_[0-9][0-9].dds.png"), recursive=True
    )
    for png in pngs:
        convert_png_to_dds(png, imagemagick_convert_path)

def generate_narc(
    src_path, dst_path, original_path, output_narc_dir, narchive_path
):
    print(f"[-] Generate narchive file from {original_path}...")
    temp_dir_par = path_join(TEMP_DIR_PAR, str(UUID(bytes=urandom(16), version=4)))
    temp_dir = path_join(temp_dir_par, "tmp")
    makedirs(abspath(temp_dir), exist_ok=True)
    for item in listdir(path_join(src_path, original_path)):
        if (
            item.endswith(".fif.json")
            or item.endswith(".png")
            or item.endswith("_tppk_extracted")
        ):
            continue
        copyfile(
            path_join(path_join(src_path, original_path), item),
            path_join(temp_dir, item),
        )
    output_narc_dir = path_join(dst_path, output_narc_dir[: -len("_narc_extracted")])
    mkdir_parent(output_narc_dir)
    cmd = f'{narchive_path} create "{output_narc_dir}" "{temp_dir_par}"'
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    print_process(process, CONSOLE_ENCODING)
    rmtree(temp_dir_par)


def process_text_json(text_json_file, args):
    base = basename(text_json_file)[: -len("English.json")]
    text_json_file_par = abspath(path_join(text_json_file, pardir))
    for extracted_narc in listdir(text_json_file_par):
        m = re.compile(f"{base}(_F[0-9])?English.narc_narc_extracted")
        if not m.search(extracted_narc):
            continue
        extracted_narc = abspath(path_join(text_json_file_par, extracted_narc))
        tmp_path = path_join(extracted_narc, "tmp")
        fifs = glob.glob(
            path_join(tmp_path, "**", f"{base}English_[0-9][0-9]_*.fif.json"),
            recursive=True,
        )
        for fif_path in fifs:
            update_fif_data(
                fif_path,
                base,
                text_json_file,
                tmp_path,
                args.font,
                args.alternative_font,
                args.imagemagick_convert_path,
            )
        generate_narc(
            args.dir_path,
            args.output_path,
            tmp_path[len(abspath(args.dir_path)) + 1 :],
            abspath(path_join(tmp_path, pardir))[
                len(abspath(args.dir_path)) + 1 :
            ],
            args.narchive_path
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate mtx, fif, dds, narc files")
    parser.add_argument(
        "-d",
        "--dir_path",
        help="directory path to convert",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output_path",
        help="data_steam directory path of output data",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--imagemagick_convert_path",
        help="ImageMagick convert path",
        required=True,
    )
    parser.add_argument("-n", "--narchive_path", help="Narchive path", required=True)
    parser.add_argument("-t", "--tppk_tool_path", help="TppkTool path", required=True)
    parser.add_argument(
        "-f", "--font", help="Font file path to generate font image", required=True
    )
    parser.add_argument(
        "-a", "--alternative_font",
        help="Font file path to generate font image if current font cannot render the glyph",
        required=True
    )

    args = parser.parse_args()

    # process font data
    text_json_files = glob.glob(
        path_join(args.dir_path, "**", "*English.json"), recursive=True
    )
    
    with Pool(processes=8) as pool:
        pool.map(partial(process_text_json, args=args), text_json_files)
        

