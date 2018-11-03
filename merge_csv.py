import csv
from collections import OrderedDict

debug = False

data = OrderedDict()
with open("data\\text_steam.csv", newline="", encoding="utf-8") as f:
    csv_reader = csv.reader(f)
    is_header = True
    index = 0
    for row in csv_reader:
        index = index + 1
        if is_header:
            is_header = False
            continue
        key = row[0]
        en = row[1]
        jp = row[2]

        skey = key.split("|")
        json_path = skey[0][1:]
        entry_wrapper_index = int(skey[1])
        entry_index = int(skey[2])

        if json_path not in data:
            data[json_path] = {}
        if entry_wrapper_index not in data[json_path]:
            data[json_path][entry_wrapper_index] = {}

        data[json_path][entry_wrapper_index][entry_index] = {
            "en": f"{en}",
            "jp": f"{jp}",
        }

with open("data\\text_switch.csv", newline="", encoding="utf-8") as f:
    csv_reader = csv.reader(f)
    is_header = True
    index = 0
    for row in csv_reader:
        index = index + 1
        if is_header:
            is_header = False
            continue
        key = row[0]
        kr = row[3]

        skey = key.split("|")
        json_path = skey[0][1:]
        entry_wrapper_index = int(skey[1])
        entry_index = int(skey[2])

        if json_path not in data:
            data[json_path] = {}
        if entry_wrapper_index not in data[json_path]:
            data[json_path][entry_wrapper_index] = {}

        if entry_index in data[json_path][entry_wrapper_index]:
            data[json_path][entry_wrapper_index][entry_index]["s2_kr"] = f"{kr}"
        else:
            data[json_path][entry_wrapper_index][entry_index] = {
                "s2_kr": f"{kr}",
            }

with open("data\\text_merge.csv", "w", newline="", encoding="utf-8") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["Key", "한국어(패치)", "한국어(스위치)", "영어(스팀)", "일본어(스팀)",])
    for json_path in sorted(data.keys()):
        for entry_wrapper_index in sorted(data[json_path].keys()):
            for entry_index in sorted(data[json_path][entry_wrapper_index].keys()):
                el = data[json_path][entry_wrapper_index][entry_index]
                csv_writer.writerow(
                    [
                        f"{json_path}|{entry_wrapper_index}|{entry_index}",
                        "",
                        el["s2_kr"] if "s2_kr" in el else "",
                        el["en"] if "en" in el else "",
                        el["jp"] if "jp" in el else "",
                    ]
                )