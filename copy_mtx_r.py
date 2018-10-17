import argparse
import glob
from locale import getdefaultlocale
from os import pardir, sep
from os.path import isdir, abspath
from os.path import join as path_join
from subprocess import Popen, PIPE
from shutil import copyfile

from app.utils.io import print_process

CONSOLE_ENCODING = getdefaultlocale()[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="copy mtx files recursively"
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

    all_files = glob.glob(path_join(source_path, "**", "*.mtx"), recursive=True)
    for file in all_files:
        rel_file = abspath(file)[len(source_path):]
        print(f"[-] Copy {rel_file}")
        copyfile(source_path + rel_file, destination_path + rel_file)
        
    