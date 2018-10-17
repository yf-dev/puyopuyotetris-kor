import argparse
import glob
from os.path import join as path_join
from os.path import abspath, basename, isfile
from os import makedirs, pardir, remove, listdir
from subprocess import Popen, PIPE
from tempfile import gettempdir
from shutil import rmtree, copyfile
import re
import sys
from locale import getdefaultlocale
from app.utils.io import print_process

CONSOLE_ENCODING = getdefaultlocale()[1]

TEMP_DIR_PAR = path_join(gettempdir(), "puyopuyotetris-tempdata")
TEMP_DIR = path_join(TEMP_DIR_PAR, "tmp")


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
    fif_path, base, text_json_file, narc_tmp_path, font, imagemagick_convert_path
):
    index = int(basename(fif_path)[len(f"{base}English_") :][:2], base=10)
    fif_base = fif_path[: -len(".fif.json")]
    if getattr(sys, "frozen", False):
        fif_command = f"generate_font_data.exe {text_json_file} {narc_tmp_path} {fif_base} -f {fif_path} -g {font} -i {index}"
    else:
        fif_command = f"python generate_font_data.py {text_json_file} {narc_tmp_path} {fif_base} -f {fif_path} -g {font} -i {index}"
    print(f"[-] Generate fif file and font images from {fif_path}...")
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


def update_mtx_data(src_path, dst_path, text_json_file, mtx_to_json_path):
    output_path = path_join(dst_path, text_json_file[len(src_path) + 1 : -4] + "mtx")
    mkdir_parent(output_path)

    print(f"[-] Convert {text_json_file} to mtx...")

    process = Popen(
        f"{mtx_to_json_path} -f mtx -o {output_path} {text_json_file}",
        stdout=PIPE,
        stderr=PIPE,
    )
    print_process(process, CONSOLE_ENCODING)


def generate_narc(
    src_path, dst_path, original_path, output_narc_dir, narchive_path, is_use_tmp=False
):
    if is_use_tmp:
        parent_dir = TEMP_DIR_PAR
    else:
        parent_dir = TEMP_DIR
    print(f"[-] Generate narchive file from {original_path}...")
    mkdir_parent(path_join(TEMP_DIR, "noname"))
    for item in listdir(path_join(src_path, original_path)):
        if (
            item.endswith(".fif.json")
            or item.endswith(".png")
            or item.endswith("_tppk_extracted")
        ):
            continue
        copyfile(
            path_join(path_join(src_path, original_path), item),
            path_join(TEMP_DIR, item),
        )
    output_narc_dir = path_join(dst_path, output_narc_dir[: -len("_extracted")])
    mkdir_parent(output_narc_dir)
    cmd = f'{narchive_path} create "{output_narc_dir}" "{parent_dir}"'
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    print_process(process, CONSOLE_ENCODING)
    rmtree(TEMP_DIR)


def generate_tppk(original_path, tppk_tool_path):
    print(f"[-] Generate tppk file from {original_path}...")
    mkdir_parent(path_join(TEMP_DIR, "noname"))
    for item in listdir(original_path):
        if item.endswith(".png"):
            continue
        copyfile(path_join(original_path, item), path_join(TEMP_DIR, item))
    output_tppk_dir = original_path[: -len("_tppk_extracted")]
    process = Popen(
        f'{tppk_tool_path} create "{output_tppk_dir}" "{TEMP_DIR}"',
        stdout=PIPE,
        stderr=PIPE,
    )
    print_process(process, CONSOLE_ENCODING)
    rmtree(TEMP_DIR)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate mtx, fif, dds, narc files")
    parser.add_argument(
        "-a",
        "--font_data",
        help="data_steam directory path of font data to convert",
        required=True,
    )
    parser.add_argument(
        "-b",
        "--image_data",
        help="data_steam directory path of image data to convert",
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
    parser.add_argument(
        "-m", "--mtx_to_json_path", help="MtxToJson path", required=True
    )
    parser.add_argument("-n", "--narchive_path", help="Narchive path", required=True)
    parser.add_argument("-t", "--tppk_tool_path", help="TppkTool path", required=True)
    parser.add_argument(
        "-f", "--font", help="Font file path to generate font image", required=True
    )
    parser.add_argument("--skip_font_data", help="Skip font generate", action="store_true")
    parser.add_argument("--skip_image_data", help="Skip image generate", action="store_true")

    args = parser.parse_args()

    # process font data
    if not args.skip_font_data:
        text_json_files = glob.glob(
            path_join(args.font_data, "**", "*English.json"), recursive=True
        )
        for text_json_file in text_json_files:
            base = basename(text_json_file)[: -len("English.json")]
            text_json_file_par = abspath(path_join(text_json_file, pardir))
            for extracted_narc in listdir(text_json_file_par):
                m = re.compile(f"{base}(_F[0-9])?English.narc_extracted")
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
                        args.imagemagick_convert_path,
                    )
                generate_narc(
                    args.font_data,
                    args.output_path,
                    tmp_path[len(abspath(args.font_data)) + 1 :],
                    abspath(path_join(tmp_path, pardir))[
                        len(abspath(args.font_data)) + 1 :
                    ],
                    args.narchive_path,
                    is_use_tmp=True,
                )

            update_mtx_data(
                args.font_data, args.output_path, text_json_file, args.mtx_to_json_path
            )

    # process image data
    if not args.skip_image_data:
        png_files = glob.glob(path_join(args.image_data, "**", "*.png"), recursive=True)
        for png_file in png_files:
            convert_png_to_dds(png_file, args.imagemagick_convert_path)

        extracted_tppks = glob.glob(
            path_join(args.image_data, "**", "*_tppk_extracted"), recursive=True
        )
        for extracted_tppk in extracted_tppks:
            generate_tppk(extracted_tppk, args.tppk_tool_path)

        extracted_narcs = glob.glob(
            path_join(args.image_data, "**", "*narc_extracted"), recursive=True
        )
        for extracted_narc in extracted_narcs:
            p = extracted_narc[len(args.image_data) + 1 :]
            generate_narc(args.image_data, args.output_path, p, p, args.narchive_path)
