import argparse
import glob
from locale import getdefaultlocale
from os.path import join as path_join
from subprocess import Popen, PIPE

from app.utils.io import print_process
from multiprocessing import Pool
from functools import partial

CONSOLE_ENCODING = getdefaultlocale()[1]

def mtx_to_json(json_file, mtx_to_json_path):
    if json_file.endswith(".fif.json"):
        return
    print(f"[-] Converting {json_file} to mtx")
    process = Popen(
        f"{mtx_to_json_path} {json_file}", stdout=PIPE, stderr=PIPE
    )
    print_process(process, CONSOLE_ENCODING)

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
    mtx_to_json_i = partial(mtx_to_json, mtx_to_json_path=args.mtx_to_json_path)
    with Pool(processes=16) as pool:
        pool.map(mtx_to_json_i, json_files)