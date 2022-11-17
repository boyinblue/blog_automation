#!/usr/bin/env python3

import os
import pickle
import re

""" 철지난 이벤트 파일들을 삭제한다. """
""" 종료일별로 이벤트를 수집한다. """

p_due_date = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")

def load_dic(filename):
    f = open(filename, 'rb')
    dic = pickle.load(f, encoding='bytes')
    return dic

def save_dic(filename, dic):
    with open(filename, "wb") as f:
        pickle.dump(dic, f)

def check_due_date(dic):
    due_date = p_due_date.findall(dic['period'])
    print("Date Changed", dic['period'], due_date)

files = os.listdir("tmp")
for file in files:
    path = "tmp/{}".format(file)
    if not file.endswith(".pkl"):
        continue
    dic = load_dic(path)
    check_due_date(dic)
    print(dic)
