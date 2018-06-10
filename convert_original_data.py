from subprocess import Popen, PIPE
import argparse
import glob
import json
from os.path import basename, isdir
from os.path import join as path_join
from app.models.fif import FifFile


def print_process(process):
    stdout, stderr = process.communicate()
    if stdout:
        print(stdout.decode("utf-8"))
    if stderr:
        print(stderr.decode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert narc, mtx, fif file to readable format"
    )
    parser.add_argument("path", help="Directory to convert")
    parser.add_argument(
        "-m", "--mtx_to_json_path", help="MtxToJson path", required=True
    )
    parser.add_argument("-n", "--narchive_path", help="Narchive path", required=True)
    parser.add_argument("-t", "--tppk_tool_path", help="TppkTool path", required=True)
    parser.add_argument(
        "-i",
        "--imagemagick_convert_path",
        help="ImageMagick convert path",
        required=True,
    )
    args = parser.parse_args()

    narc_files = glob.glob(path_join(args.path, "**", "*.narc"), recursive=True)
    for narc_file in narc_files:
        print(f"[-] Extracting {narc_file} ...")
        process = Popen(
            f"{args.narchive_path} extract -o {narc_file}_extracted {narc_file}",
            stdout=PIPE,
            stderr=PIPE,
        )
        print_process(process)

    mtx_files = glob.glob(path_join(args.path, "**", "*.mtx"), recursive=True)
    for mtx_file in mtx_files:
        print(f"[-] Converting {mtx_file} to json")
        process = Popen(f"{args.mtx_to_json_path} {mtx_file}", stdout=PIPE, stderr=PIPE)
        print_process(process)

    fif_files = glob.glob(path_join(args.path, "**", "*.fif"), recursive=True)
    for fif_file in fif_files:
        print(f"[-] Converting {fif_file} to json")
        fif = FifFile.load(fif_file)
        obj = fif.export_obj()
        target_path = fif_file + ".json"
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False, indent=True))

    all_files = glob.glob(path_join(args.path, "**", "*"), recursive=True)
    for a_file in all_files:
        if isdir(a_file) or "." in basename(a_file):
            continue
        extensionless_file = a_file
        with open(extensionless_file, "rb") as f:
            magic_code = f.read(4)
            if magic_code != b"tppk":
                continue
            print(f"[-] Extracting TPPK {extensionless_file} ...")
            process = Popen(
                f"{args.tppk_tool_path} extract -o {extensionless_file}_tppk_extracted {extensionless_file}",
                stdout=PIPE,
                stderr=PIPE,
            )
            print_process(process)

    dds_files = glob.glob(path_join(args.path, "**", "*.dds"), recursive=True)
    for dds_file in dds_files:
        print(f"[-] Converting {dds_file} to png")
        process = Popen(
            f"{args.imagemagick_convert_path} dds:{dds_file} {dds_file}.png",
            stdout=PIPE,
            stderr=PIPE,
        )
        print_process(process)

    dat_files = glob.glob(path_join(args.path, "**", "*.dat"), recursive=True)
    for dat_file in dat_files:
        with open(dat_file, "rb") as f:
            magic_code = f.read(3)
            if magic_code != b"DDS":
                continue
            print(f"[-] Converting {dat_file} to png")
            process = Popen(
                f"{args.imagemagick_convert_path} dds:{dat_file} {dat_file}.png",
                stdout=PIPE,
                stderr=PIPE,
            )
            print_process(process)

    for a_file in all_files:
        if isdir(a_file) or "." in basename(a_file):
            continue
        extensionless_file = a_file
        with open(extensionless_file, "rb") as f:
            magic_code = f.read(3)
            if magic_code != b"DDS":
                continue
            print(f"[-] Convert extensionless DDS to PNG {extensionless_file} ...")
            process = Popen(
                f"{args.imagemagick_convert_path} dds:{extensionless_file} {extensionless_file}.png",
                stdout=PIPE,
                stderr=PIPE,
            )
            print_process(process)
