import json
from collections import defaultdict
import os


def convert():
    json_obj = defaultdict(list)
    cwd = os.getcwd()
    with open("../data/dblp_final.json",  "r") as f:
        for each_line in f:
            each_obj = json.loads(each_line)
            univ_name = each_obj["univ_name"]
            del each_obj["univ_name"]
            json_obj[univ_name].append(each_obj)
    with open("../data/dblp_final_JSON.json", "w+") as f:
        f.write(json.dumps(json_obj, sort_keys=True, indent=4, \
                separators=(',', ': ')))


convert()
