import argparse
import glob
import json
from os.path import join as path_join
from os.path import realpath, abspath
from collections import OrderedDict
import csv
from os import makedirs, pardir


def save_to_csv(path, data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Key", "English", "Japanese", "Korean"])
        for key in data:
            el = data[key]
            csv_writer.writerow(
                [
                    key,
                    el["en"] if "en" in el else "",
                    el["jp"] if "jp" in el else "",
                    el["kr"] if "kr" in el else "",
                ]
            )


def save_to_dir(data_steam_root, data):
    for json_path in data:
        json_data = {"Has64BitOffsets": True}
        json_data["Entries"] = []
        for entry_wrapper in data[json_path]:
            entry_wrapper_o = []
            for entry in entry_wrapper:
                entry_wrapper_o.append(entry["kr"])
            json_data["Entries"].append(entry_wrapper_o)

        json_file_path = path_join(
            realpath(data_steam_root), json_path + "English.json"
        )
        makedirs(abspath(path_join(json_file_path, pardir)), exist_ok=True)
        with open(json_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False, indent=True))


def update_data_form_json(json_path, path_key, data, lang):
    with open(json_path, "r", encoding="utf-8") as json_f:
        json_data = json.load(json_f)
        for entry_wrapper_index in range(len(json_data["Entries"])):
            entry_wrapper = json_data["Entries"][entry_wrapper_index]
            for entry_index in range(len(entry_wrapper)):
                entry = entry_wrapper[entry_index].replace("\n", "\\n")
                key = f"{path_key}|{entry_wrapper_index}|{entry_index}"
                if key in data:
                    tmp = data[key]
                    tmp[lang] = entry
                    data[key] = tmp
                else:
                    data[key] = {lang: entry, "kr": ""}


def load_data_from_csv(path, use_sg=False):
    data = OrderedDict()

    with open(path, newline="", encoding="utf-8") as f:
        csv_reader = csv.reader(f)
        is_header = True
        for row in csv_reader:
            if is_header:
                is_header = False
                continue
            key = row[0]
            en = row[1].replace("\\n", "\n")
            jp = row[2].replace("\\n", "\n")
            kr = row[3].replace("\\n", "\n")
            kr_sg = row[4].replace("\\n", "\n")

            skey = key.split("|")
            json_path = skey[0][1:]
            entry_wrapper_index = skey[1]
            entry_index = skey[2]

            if not kr:
                if use_sg and kr_sg:
                    kr = kr_sg
                else:
                    kr = en
            if en:
                if json_path not in data:
                    data[json_path] = {}
                if entry_wrapper_index not in data[json_path]:
                    data[json_path][entry_wrapper_index] = {}
                data[json_path][entry_wrapper_index][entry_index] = {
                    "en": en,
                    "jp": jp,
                    "kr": kr,
                }

    # validation and convert dict to list

    for json_path in data:
        ewil = len(data[json_path].keys())
        ewi_list = []
        for entry_wrapper_index in range(ewil):
            entry_wrapper_index = str(entry_wrapper_index)
            if entry_wrapper_index not in data[json_path]:
                raise Exception(
                    f"entry_wrapper_index {entry_wrapper_index} is not defined in {json_path}"
                )
            eil = len(data[json_path][entry_wrapper_index].keys())
            ei_list = []
            for entry_index in range(eil):
                entry_index = str(entry_index)
                if entry_index not in data[json_path][entry_wrapper_index]:
                    raise Exception(
                        f"entry_index {entry_index} is not defined in {json_path} on entry_wrapper_index {entry_wrapper_index}"
                    )
                ei_list.append(data[json_path][entry_wrapper_index][entry_index])
            ewi_list.append(ei_list)
        data[json_path] = ewi_list

    return data


def load_data_from_dir(path, data_steam_root):
    data = OrderedDict()

    en_json_files = glob.glob(path_join(path, "**", "*English.json"), recursive=True)
    for en_json_file in en_json_files:
        path_key = en_json_file[len(data_steam_root) : -len("English.json")]
        update_data_form_json(en_json_file, path_key, data, "en")

    jp_json_files = glob.glob(path_join(path, "**", "*Japanese.json"), recursive=True)
    for jp_json_file in jp_json_files:
        path_key = jp_json_file[len(data_steam_root) : -len("Japanese.json")]
        update_data_form_json(jp_json_file, path_key, data, "jp")

    json_files = glob.glob(path_join(path, "**", "*.json"), recursive=True)
    for json_file in json_files:
        if json_file.endswith(".fif.json"):
            continue
        elif json_file.endswith("English.json"):
            path_key = json_file[len(data_steam_root) : -len("English.json")]
        elif json_file.endswith("Japanese.json"):
            path_key = json_file[len(data_steam_root) : -len("Japanese.json")]
        else:
            continue

        update_data_form_json(json_file, path_key, data, "jp")

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert all text in the game to csv for translation or vice versa"
    )
    parser.add_argument(
        "convert",
        choices=["json", "csv"],
        help="Target format to convert from current data",
    )
    parser.add_argument("path", help="Directory to convert")
    parser.add_argument("data_steam_root", help="Directory path of data_steam root")
    parser.add_argument("csv", help="File path of csv")
    parser.add_argument(
        "--use_suggestion",
        help="Use suggestion text if korean text is empty",
        action="store_true",
    )
    args = parser.parse_args()

    if args.convert == "csv":
        data = load_data_from_dir(args.path, args.data_steam_root)
        save_to_csv(args.csv, data)
    else:
        data = load_data_from_csv(args.csv, args.use_suggestion)
        save_to_dir(args.data_steam_root, data)
