import argparse
import glob
from locale import getdefaultlocale
from os import pardir
from os.path import isdir, abspath
from os.path import join as path_join
from subprocess import Popen, PIPE

from app.utils.io import print_process

CONSOLE_ENCODING = getdefaultlocale()[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="convert bntx files to dds recursively"
    )
    parser.add_argument(
        "-d",
        "--dir_path",
        help="directory path to convert",
        required=True,
    )
    parser.add_argument(
        "-b",
        "--bntx_script_path",
        help="bntx extractor script path",
        required=True
    )

    args = parser.parse_args()

    bntx_script_path = abspath(args.bntx_script_path)

    all_files = glob.glob(path_join(args.dir_path, "**", "*"), recursive=True)
    for file in all_files:
        file = abspath(file)
        if isdir(file):
            continue
        with open(file, "rb") as f:
            magic_code = f.read(4)
            if magic_code != b"BNTX":
                continue
            file_parent = abspath(path_join(file, pardir))
            print(f"[-] convert {file}")
            process = Popen(
                f"python {bntx_script_path} {file}",
                cwd=file_parent,
                stdout=PIPE,
                stderr=PIPE,
            )
            print_process(process, CONSOLE_ENCODING)

