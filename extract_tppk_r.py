import argparse
import glob
from locale import getdefaultlocale
from os.path import isdir
from os.path import join as path_join
from subprocess import Popen, PIPE

from app.utils.io import print_process

CONSOLE_ENCODING = getdefaultlocale()[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="extract tppk files recursively")
    parser.add_argument(
        "-d",
        "--dir_path",
        help="directory path to extract",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--tppk_tool_path",
        help="TppkTool path",
        required=True
    )

    args = parser.parse_args()

    all_files = glob.glob(path_join(args.dir_path, "**", "*"), recursive=True)
    for file in all_files:
        if isdir(file):
            continue
        with open(file, "rb") as f:
            magic_code = f.read(4)
            if magic_code != b"tppk":
                continue
            print(f"[-] Extract {file}")
            process = Popen(
                f"{args.tppk_tool_path} extract -o {file}_tppk_extracted {file}",
                stdout=PIPE,
                stderr=PIPE,
            )
            print_process(process, CONSOLE_ENCODING)
