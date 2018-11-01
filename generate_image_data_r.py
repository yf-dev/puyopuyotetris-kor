import argparse
import glob
from os.path import join as path_join
from os.path import abspath, basename, isfile, dirname
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
            or item.endswith(".psd")
            or item.endswith("_tppk_extracted")
        ):
            continue
        copyfile(
            path_join(path_join(src_path, original_path), item),
            path_join(TEMP_DIR, item),
        )
    output_narc_dir = path_join(dst_path, output_narc_dir[: -len("_narc_extracted")])
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
        elif item.endswith(".psd"):
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
    parser = argparse.ArgumentParser(description="generate dds, narc files")
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

    args = parser.parse_args()

    all_files = glob.glob(path_join(args.dir_path, "**", "*"), recursive=True)
    for f in all_files:
        if "_tppk_extracted" in f or "_narc_extracted" in f:
            continue
        if isfile(f):
            if (
                f.endswith(".fif.json")
                or f.endswith(".png")
                or f.endswith(".psd")
                or f.endswith(".tppk")
                or f.endswith(".narc")
            ):
                continue
            path = abspath(f)[len(abspath(args.dir_path)):]
            dest_path = abspath(args.output_path) + path
            print(dest_path)
            makedirs(dirname(dest_path), exist_ok=True)
            copyfile(f, dest_path)


    png_files = glob.glob(path_join(args.dir_path, "**", "*.png"), recursive=True)
    for png_file in png_files:
        convert_png_to_dds(png_file, args.imagemagick_convert_path)

    extracted_tppks = glob.glob(
        path_join(args.dir_path, "**", "*_tppk_extracted"), recursive=True
    )
    for extracted_tppk in extracted_tppks:
        generate_tppk(extracted_tppk, args.tppk_tool_path)

    extracted_narcs = glob.glob(
        path_join(args.dir_path, "**", "*_narc_extracted"), recursive=True
    )
    for extracted_narc in extracted_narcs:
        p = extracted_narc[len(args.dir_path) + 1 :]
        generate_narc(args.dir_path, args.output_path, p, p, args.narchive_path)