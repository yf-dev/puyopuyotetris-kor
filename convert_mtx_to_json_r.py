import argparse
import glob
from locale import getdefaultlocale
from os.path import join as path_join
from subprocess import Popen, PIPE

from app.utils.io import print_process

CONSOLE_ENCODING = getdefaultlocale()[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="convert mtx files to json recursively"
    )
    parser.add_argument(
        "-d",
        "--dir_path",
        help="directory path to convert",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--mtx_to_json_path",
        help="MtxToJson path",
        required=True
    )

    args = parser.parse_args()

    mtx_files = glob.glob(path_join(args.dir_path, "**", "*.mtx"), recursive=True)
    for mtx_file in mtx_files:
        print(f"[-] Converting {mtx_file} to json")
        process = Popen(
            f"{args.mtx_to_json_path} {mtx_file}", stdout=PIPE, stderr=PIPE
        )
        print_process(process, CONSOLE_ENCODING)