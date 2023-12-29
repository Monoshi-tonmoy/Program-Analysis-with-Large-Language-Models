import os
import sys
import json
import random

def add_pythonpath(path):
    if path not in sys.path:
        sys.path.append(path)


root_dir = os.getcwd().split("prompting")[0]
project_dir = f"{root_dir}/prompting/"
data_dir = f"{project_dir}/data"

def read_jsonl(datapath):
    f  = open(datapath, "r")
    data = [json.loads(ex) for ex in f]
    f.close()
    return data


def get_k_smallest_data(datapath, k=20):
    data = read_jsonl(datapath)
    data = sorted(data, key=lambda x: len(x['func'].split()))

    vul, nvul = [], []
    for ex in data:
        if len(ex['func'].split("\n")) < 10:
            continue
        if len(ex['func'].split("\n")) > 30:
            continue
        if ex['target'] == 0:
            nvul.append(ex)
        else:
            vul.append(ex)
    return random.sample(vul, k) + random.sample(nvul, k)


def write_file(path, data):
    folder = os.path.dirname(path)

    if folder != '' and not os.path.exists(folder):
        os.makedirs(folder)
    if len(data) == 0:
        return
    if isinstance(data, list):
        if isinstance(data[0], dict):
            data = '\n'.join([json.dumps(ex) for ex in data])
        else:
            data = '\n'.join(data)
    f = open(path, 'w', encoding='utf-8')
    f.write(data)
    f.close()
