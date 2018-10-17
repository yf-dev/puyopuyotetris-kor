import argparse
import glob
from locale import getdefaultlocale
from os.path import join as path_join
from subprocess import Popen, PIPE

from app.utils.io import print_process

CONSOLE_ENCODING = getdefaultlocale()[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="convert json files to mtx recursively"
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

    json_files = glob.glob(path_join(args.dir_path, "**", "*.json"), recursive=True)
    for json_file in json_files:
        if json_file.endswith(".fif.json"):
            continue
        print(f"[-] Converting {json_file} to mtx")
        process = Popen(
            f"{args.mtx_to_json_path} {json_file}", stdout=PIPE, stderr=PIPE
        )
        print_process(process, CONSOLE_ENCODING)
