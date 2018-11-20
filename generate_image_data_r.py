import argparse
import glob
from os.path import join as path_join
from os.path import abspath, basename, isfile, dirname
from os import makedirs, pardir, remove, listdir, urandom
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
            or item.endswith(".psd")
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


def generate_tppk(original_path, tppk_tool_path):
    print(f"[-] Generate tppk file from {original_path}...")
    temp_dir = path_join(TEMP_DIR_PAR, str(UUID(bytes=urandom(16), version=4)))
    makedirs(abspath(temp_dir), exist_ok=True)
    for item in listdir(original_path):
        if item.endswith(".png"):
            continue
        elif item.endswith(".psd"):
            continue
        copyfile(path_join(original_path, item), path_join(temp_dir, item))
    output_tppk_dir = original_path[: -len("_tppk_extracted")]
    process = Popen(
        f'{tppk_tool_path} create "{output_tppk_dir}" "{temp_dir}"',
        stdout=PIPE,
        stderr=PIPE,
    )
    print_process(process, CONSOLE_ENCODING)
    rmtree(temp_dir)

def process_generate_narc(extracted_narc, args):
    p = extracted_narc[len(args.dir_path) + 1 :]
    generate_narc(args.dir_path, args.output_path, p, p, args.narchive_path)

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

    png_files = glob.glob(path_join(args.dir_path, "**", "*.png"), recursive=True)
    with Pool(processes=8) as pool:
        pool.map(partial(
            convert_png_to_dds, 
            imagemagick_convert_path=args.imagemagick_convert_path
        ), png_files)

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

    extracted_tppks = glob.glob(
        path_join(args.dir_path, "**", "*_tppk_extracted"), recursive=True
    )
    with Pool(processes=8) as pool:
        pool.map(partial(
            generate_tppk, 
            tppk_tool_path=args.tppk_tool_path
        ), extracted_tppks)

    extracted_narcs = glob.glob(
        path_join(args.dir_path, "**", "*_narc_extracted"), recursive=True
    )
    with Pool(processes=8) as pool:
        pool.map(partial(
            process_generate_narc, 
            args=args
        ), extracted_narcs)