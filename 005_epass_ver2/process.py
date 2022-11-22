#!/usr/bin/env python3

""" 철지난 이벤트 파일들을 삭제한다. """
""" 종료일별로 이벤트를 수집한다. """

import os
import pickle
import re
from datetime import datetime
import sys
import glob

MD_FILE_SAVE_PATH = "../../boyinblue.github.io/_posts/event/"

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
def delete_expired_file(filename):
    title, ext = os.path.splitext(filename)
    files = glob.glob("{}.*".format(title))
    for file in files:
        os.remove(file)
#    os.remove("{}.*".format(title))

def write_info_by_exp_date(dic):
    try:
        dic['md']
    except:
        print("There is no md key")
        return
    exp_date_str = get_string_from_date(dic['period'])
    info_fname_by_exp_dat = "{}{}-event.md".format(MD_FILE_SAVE_PATH, exp_date_str)
    if not os.path.exists(info_fname_by_exp_dat):
        fp = open(info_fname_by_exp_dat, "w")
        fp.write("---\n")
        fp.write("title: {} 종료되는 이벤트 정보\n".format(exp_date_str))
        fp.write("description: {}에 종료되는 이벤트 정보들을 제공합니다.\n".format(exp_date_str))
        fp.write("category: event\n")
        fp.write("image: /assets/images/event/logo.png\n")
        fp.write("---\n")
        fp.write(dic['md'])
        return
    fp = open(info_fname_by_exp_dat, "r")
    lines = fp.readlines()
    fp.close()

    for line in lines:
        if line.__contains__(dic['url']):
            return
    
    fp = open(info_fname_by_exp_dat, "a")
    fp.write("\n")
    fp.write("<hr>")
    fp.write(dic['md'])
    fp.close()

def check_due_date(dic, filename):
    dic_date = dic['period']
    today = get_today_date()
    if dic_date < today:
        print("delete expired event")
        delete_expired_file(filename)
    elif dic_date == today:
        print("Will be expired today")
    else:
        print("Will be expired {}".format(get_string_from_date(dic_date)))

def check_pkl_file(filename):
    if not filename.endswith(".pkl"):
        return
    print("ID :", filename)
    dic = load_dic(filename)
    check_due_date(dic, filename)
    write_info_by_exp_date(dic)
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
