#!/usr/bin/env python3

""" 철지난 이벤트 파일들을 삭제한다. """
""" 종료일별로 이벤트를 수집한다. """

import os
import pickle
import re
from datetime import datetime
import sys

""" Dictionary 저장 및 로드 관련 """
def load_dic(filename):
    f = open(filename, 'rb')
    dic = pickle.load(f, encoding='bytes')
    return dic

def save_dic(filename, dic):
    f = open(filename, 'wb')
    pickle.dump(dic, f)

""" 날짜 관련 함수들 """
def get_string_from_date(date):
    return date.strftime("%Y-%m-%d")

def get_date_from_string(str):
    return datetime.strptime(str, "%Y-%m-%d")

def get_today_date():
    now = datetime.now()
    return now

""" Dictionary 데이터를 관리한다. """
def check_due_date(dic, filename):
    if type(dic['period']) is str:
        dic['period'] = get_date_from_string(dic['period'])
        save_dic(filename, dic)

def check_pkl_file(filename):
    if not filename.endswith(".pkl"):
        return
    print("ID :", filename)
    dic = load_dic(filename)
    check_due_date(dic, filename)
#    print(dic)

""" 메인 함수 """
def main():
    """ 인자를 직접 받아서 처리하는 경우 """
    if len(sys.argv) > 1:
        check_pkl_file(sys.argv[1])
        return

    """ tmp 디렉토리에 있는 모든 파일을 탐색하여 처리 """
    files = os.listdir("tmp")
    for file in files:
        path = "tmp/{}".format(file)
        check_pkl_file(path)

if __name__ == '__main__':
    main()
