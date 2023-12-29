import os
import sys
import json
import pandas
import random
import dataclasses
import tree_sitter
from typing import Set
from tree_sitter_languages import get_parser
import pandas as pd


def add_pythonpath(path):
    if path not in sys.path:
        sys.path.append(path)


root_dir = os.getcwd().split("prompting")[0]
project_dir = f"{root_dir}/prompting/"
data_dir = f"{project_dir}/data"

def read_data(datapath):
    f  = open(datapath, "r")
    data = [json.loads(ex) for ex in f]
    f.close()
    return data


def get_k_smallest_data(datapath, k=20):
    data = read_data(datapath)
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
    if not os.path.exists(folder):
        os.makedirs(folder)
    if len(data) == 0:
        return
    if isinstance(data, list):
        if isinstance(data[0], dict):
            data = '\n'.join([json.dumps(ex) for ex in data])
        else:
            data = '\n'.join(data)
    f = open(path, 'w')
    f.write(data)
    f.close()


def get_children(node, fn, reverse=False):
    it = node.children
    if reverse:
        it = reversed(it)
    if isinstance(fn, str):
        fn_str = str(fn)
        fn = lambda n: n.type == fn_str
    return [c for c in it if fn(c)]

def get_child(node, fn, reverse=False):
    return next(iter(get_children(node, fn, reverse=reverse)), None)

def is_type(typename):
    def fn(n):
        return n.type == typename
    return fn


def extract_api_calls(tree):
    api_names = []
    q = [tree.root_node]
    while len(q) > 0:
        n = q.pop()
        if n.type == "call_expression":
            ident = get_child(n, "identifier")
            if ident is not None:
                call_name = ident.text.decode()
                api_names.append(call_name)
        if n.type not in ("string_literal", "char_literal"):
            q.extend(reversed(list(n.children)))
    return api_names


parser = get_parser("c")
def get_api_names(code):
    if isinstance(code, str):
        code = code.encode()
    tree = parser.parse(code)
    # print_tree(tree.root_node)
    return extract_api_calls(tree)
