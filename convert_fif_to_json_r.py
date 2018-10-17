import argparse
import glob
import json
from locale import getdefaultlocale
from os.path import join as path_join
from app.models.fif import FifFile

CONSOLE_ENCODING = getdefaultlocale()[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="convert fif files to json recursively"
    )
    parser.add_argument(
        "-d",
        "--dir_path",
        help="directory path to convert",
        required=True,
    )

    args = parser.parse_args()

    fif_files = glob.glob(path_join(args.dir_path, "**", "*.fif"), recursive=True)
    for fif_file in fif_files:
        print(f"[-] Converting {fif_file} to json")
        fif = FifFile.load(fif_file)
        obj = fif.export_obj()
        target_path = fif_file + ".json"
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False, indent=True))