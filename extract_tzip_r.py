import argparse
import glob
from locale import getdefaultlocale
from os import pardir
from os.path import join as path_join
from subprocess import Popen, PIPE
from app.utils.io import print_process

CONSOLE_ENCODING = getdefaultlocale()[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="extract tzip files recursively")
    parser.add_argument(
        "-d",
        "--dir_path",
        help="directory path to extract",
        required=True,
    )
    parser.add_argument(
        "-q",
        "--quickbms_path",
        help="quickbms path",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--quickbms_script",
        help="quickbms script path",
        required=True,
    )

    args = parser.parse_args()

    tzip_files = glob.glob(path_join(args.dir_path, "**", "*.tzip"), recursive=True)
    for tzip_file in tzip_files:
        print(f"[-] Extract {tzip_file}")
        tzip_parent = path_join(tzip_file, pardir)
        with open(tzip_file, "rb") as f:
            process = Popen(
                f"{args.quickbms_path} -o {args.quickbms_script}"
                f" {tzip_file} {tzip_parent}",
                stdout=PIPE,
                stderr=PIPE,
            )
            print_process(process, CONSOLE_ENCODING)
