import argparse
import glob
from locale import getdefaultlocale
from os import pardir, sep
from os.path import isdir, abspath
from os.path import join as path_join
from subprocess import Popen, PIPE
from shutil import copytree, rmtree

from app.utils.io import print_process

CONSOLE_ENCODING = getdefaultlocale()[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="copy font related files recursively"
    )
    parser.add_argument(
        "-s",
        "--source_path",
        help="path of source directory",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--destination_path",
        help="path of destination directory",
        required=True
    )

    args = parser.parse_args()

    source_path = abspath(args.source_path)
    destination_path = abspath(args.destination_path)

    all_files = glob.glob(path_join(destination_path, "**", "*.mtx"), recursive=True)
    for file in all_files:
        rel_file = abspath(file)[len(destination_path):]
        dir_prefix = rel_file[:-len("English.mtx")]
        dir_prefix_a = sep.join(dir_prefix.split(sep)[:-1])
        dir_prefix_b = dir_prefix[len(dir_prefix_a) + 1:]
        extracted_dirs = glob.glob(path_join(source_path + dir_prefix_a, "**", f"{dir_prefix_b}*English.narc_narc_extracted"), recursive=True)
        for extracted_dir in extracted_dirs:
            rel_extracted_dir = abspath(extracted_dir)[len(source_path):]
            print(f"[-] Copy {source_path + rel_extracted_dir} to {destination_path + rel_extracted_dir}")
            if isdir(destination_path + rel_extracted_dir):
                rmtree(destination_path + rel_extracted_dir)
            copytree(source_path + rel_extracted_dir, destination_path + rel_extracted_dir)
        
    