import argparse
import csv
import json
from collections import OrderedDict
from os import makedirs, pardir
from os.path import join as path_join
from os.path import realpath, abspath


def save_to_dir(path, data, language, postfix, offset_64bit=False):
    for json_path in data:
        json_data = {"Has64BitOffsets": offset_64bit, "Entries": []}
        for entry_wrapper in data[json_path]:
            entry_wrapper_o = []
            for entry in entry_wrapper:
                entry_wrapper_o.append(entry[language])
            json_data["Entries"].append(entry_wrapper_o)

        json_file_path = path_join(
            realpath(path), json_path + f"{postfix}.json"
        )
        makedirs(abspath(path_join(json_file_path, pardir)), exist_ok=True)
        with open(json_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False, indent=True))


def load_data_from_csv(path, debug=False):
    data = OrderedDict()

    with open(path, newline="", encoding="utf-8") as f:
        csv_reader = csv.reader(f)
        is_header = True
        index = 0
        for row in csv_reader:
            index = index + 1
            if is_header:
                is_header = False
                continue
            key = row[0]
            en = row[1].replace("\\n", "\n")
            jp = row[2].replace("\\n", "\n")
            kr = row[3].replace("\\n", "\n")
            unknown = row[4].replace("\\n", "\n")

            skey = key.split("|")
            json_path = skey[0][1:]
            entry_wrapper_index = skey[1]
            entry_index = skey[2]

            if json_path not in data:
                data[json_path] = {}
            if entry_wrapper_index not in data[json_path]:
                data[json_path][entry_wrapper_index] = {}
            if debug:
                data[json_path][entry_wrapper_index][entry_index] = {
                    "en": f"[{index}]{en}",
                    "jp": f"[{index}]{jp}",
                    "kr": f"[{index}]{kr}",
                    "unknown": f"[{index}]{unknown}",
                }
            else:
                data[json_path][entry_wrapper_index][entry_index] = {
                    "en": f"{en}",
                    "jp": f"{jp}",
                    "kr": f"{kr}",
                    "unknown": f"{unknown}",
                }

    # validation and convert dict to list

    for json_path in data:
        ewil = len(data[json_path].keys())
        ewi_list = []
        for entry_wrapper_index in range(ewil):
            entry_wrapper_index = str(entry_wrapper_index)
            if entry_wrapper_index not in data[json_path]:
                raise Exception(
                    f"entry_wrapper_index {entry_wrapper_index}"
                    f" is not defined in {json_path}"
                )
            eil = len(data[json_path][entry_wrapper_index].keys())
            ei_list = []
            for entry_index in range(eil):
                entry_index = str(entry_index)
                if entry_index not in data[json_path][entry_wrapper_index]:
                    raise Exception(
                        f"entry_index {entry_index} is not defined in"
                        f" {json_path} on entry_wrapper_index {entry_wrapper_index}"
                    )
                ei_list.append(data[json_path][entry_wrapper_index][entry_index])
            ewi_list.append(ei_list)
        data[json_path] = ewi_list

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert csv file to mtx(json format)"
    )

    parser.add_argument(
        "-d",
        "--dir_path",
        help="target directory path to convert",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--csv",
        help="file path of csv to load",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--language",
        help="language to convert",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--postfix",
        help="postfix of mtx filename",
        required=True,
    )
    parser.add_argument(
        "--offset_64bit",
        help="set Has64BitOffsets to true",
        action="store_true",
    )
    parser.add_argument(
        "--debug",
        help="add debug text",
        action="store_true",
    )

    args = parser.parse_args()

    loaded_data = load_data_from_csv(args.csv, args.debug)
    save_to_dir(args.dir_path, loaded_data, args.language, args.postfix,
                args.offset_64bit)
