import argparse
import glob
import json
from os.path import abspath
from os.path import join as path_join
from collections import OrderedDict
import csv


def save_to_csv(path, data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Key", "English", "Japanese", "Korean", "Unknown"])
        for key in data:
            el = data[key]
            csv_writer.writerow(
                [
                    key,
                    el["en"] if "en" in el else "",
                    el["jp"] if "jp" in el else "",
                    el["kr"] if "kr" in el else "",
                    el["unknown"] if "unknown" in el else "",
                ]
            )


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
                    data[key] = {lang: entry}


def load_data_from_dir(path):
    data = OrderedDict()

    json_files = glob.glob(path_join(path, "**", "*.json"), recursive=True)
    for json_file in json_files:
        if json_file.endswith(".fif.json"):
            continue
        elif json_file.endswith("English.json"):
            path_key = json_file[len(path): -len("English.json")]
            update_data_form_json(json_file, path_key, data, "en")
            continue
        elif json_file.endswith("Japanese.json"):
            path_key = json_file[len(path): -len("Japanese.json")]
            update_data_form_json(json_file, path_key, data, "jp")
            continue
        elif json_file.endswith("Korean.json"):
            path_key = json_file[len(path): -len("Korean.json")]
            update_data_form_json(json_file, path_key, data, "kr")
            continue
        else:
            path_key = json_file[len(path): -len(".json")]
            update_data_form_json(json_file, path_key, data, "unknown")

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert all text in the game to csv for translation"
    )
    parser.add_argument(
        "-d",
        "--dir_path",
        help="directory path to convert",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--csv",
        help="file path of csv to save",
        required=True,
    )
    args = parser.parse_args()

    loaded_data = load_data_from_dir(abspath(args.dir_path))
    save_to_csv(args.csv, loaded_data)
