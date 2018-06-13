from subprocess import Popen, PIPE
import argparse
import glob
import json
from os.path import basename, isdir
from os.path import join as path_join
from app.models.fif import FifFile
from locale import getdefaultlocale
from app.utils.io import print_process

CONSOLE_ENCODING = getdefaultlocale()[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert narc, mtx, fif, tppk, dds file to readable format"
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
    parser.add_argument("--skip_narc", help="Skip narc extraction", action="store_true")
    parser.add_argument("--skip_mtx", help="Skip mtx converting", action="store_true")
    parser.add_argument("--skip_fif", help="Skip fif converting", action="store_true")
    parser.add_argument("--skip_tppk", help="Skip tppk extraction", action="store_true")
    parser.add_argument("--skip_dds", help="Skip dds converting", action="store_true")
    args = parser.parse_args()

    if not args.skip_narc:
        narc_files = glob.glob(path_join(args.path, "**", "*.narc"), recursive=True)
        for narc_file in narc_files:
            print(f"[-] Extracting {narc_file} ...")
            process = Popen(
                f"{args.narchive_path} extract -o {narc_file}_extracted {narc_file}",
                stdout=PIPE,
                stderr=PIPE,
            )
            print_process(process, CONSOLE_ENCODING)

    if not args.skip_mtx:
        mtx_files = glob.glob(path_join(args.path, "**", "*.mtx"), recursive=True)
        for mtx_file in mtx_files:
            print(f"[-] Converting {mtx_file} to json")
            process = Popen(
                f"{args.mtx_to_json_path} {mtx_file}", stdout=PIPE, stderr=PIPE
            )
            print_process(process, CONSOLE_ENCODING)

    if not args.skip_fif:
        fif_files = glob.glob(path_join(args.path, "**", "*.fif"), recursive=True)
        for fif_file in fif_files:
            print(f"[-] Converting {fif_file} to json")
            fif = FifFile.load(fif_file)
            obj = fif.export_obj()
            target_path = fif_file + ".json"
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(obj, ensure_ascii=False, indent=True))

    all_files = glob.glob(
        path_join(args.path, "**", "*"), recursive=True
    )  # tppk, dds에서 사용

    if not args.skip_tppk:
        # TPPK 파일은 확장자가 없을 수 있음. magic code를 보고 TPPK파일을 확인
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
                print_process(process, CONSOLE_ENCODING)

    if not args.skip_dds:
        dds_files = glob.glob(path_join(args.path, "**", "*.dds"), recursive=True)
        for dds_file in dds_files:
            print(f"[-] Converting {dds_file} to png")
            process = Popen(
                f"{args.imagemagick_convert_path} dds:{dds_file} {dds_file}.png",
                stdout=PIPE,
                stderr=PIPE,
            )
            print_process(process, CONSOLE_ENCODING)

        # 확장자가 DAT인 파일들을 magic code를 보고 변환함
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
                print_process(process, CONSOLE_ENCODING)


        # 확장자가 없는 파일들을 magic code를 보고 변환함
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
                print_process(process, CONSOLE_ENCODING)
