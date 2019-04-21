import json


def convert():
    json_arr = []
    with open("../data/dblp_final.json",  "r") as f:
        for each_line in f:
            each_obj = json.loads(each_line)
            json_arr.append(each_obj)
    with open("../data/dblp_final_JSON.json", "w+") as f:
        f.write(json.dumps(json_arr, sort_keys=True, indent=4, \
                separators=(',', ': ')))


convert()
