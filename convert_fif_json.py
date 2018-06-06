from collections import OrderedDict
import json
import argparse

from app.models.fif import FifFile


def convert_fif_to_json(path, target=None):
    fif = FifFile.load(path)
    obj = fif.export_obj()
    if target:
        target_path = target
    else:
        target_path = path + ".json"
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=True))


def convert_json_to_fif(path, target=None):
    if target:
        target_path = target
    else:
        target_path = path + ".json"
    with open(path, "r", encoding="utf-8") as json_f:
        obj = json.load(json_f, object_pairs_hook=OrderedDict)
        fif = FifFile.import_obj(obj)
        fif.save(target_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert fif file to json or vice versa"
    )
    parser.add_argument(
        "convert",
        choices=["json", "fif"],
        help="Target format to convert from current file",
    )
    parser.add_argument("file", help="Path of file to convert")
    parser.add_argument("-o", "--output", help="File path to save converted data")
    args = parser.parse_args()

    if args.convert == "json":
        convert_fif_to_json(args.file, args.output)
    elif args.convert == "fif":
        convert_json_to_fif(args.file, args.output)
