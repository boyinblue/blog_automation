#!/usr/bin/env python3

import url_preview
import urllib.request
import re

EPASS_URL = "https://www.e-pass.co.kr"

#p_new_data = re.compile("<a href=.*?>")
""" ID만 추출하기 위한 정규 표현식(ex : 2022-11-16-011) """
p_new_data = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{3}")

""" 순서 """
""" 1 : RAW HTML 가져오기 """
""" 2 : ID 가져오기 """
""" 3 : ID로부터 정보 가져오기 """
""" 4 : 최종 이벤트 페이지 정보 가져오기 """

def get_raw_list(url):
    with urllib.request.urlopen(url) as response:
        print("charset :", response.info().get_charset() )
        response_str = response.read().decode('euc-kr')
        return response_str

def get_ids(lines):
    ids = []
    for line in lines:
        contents = p_new_data.findall(line)
        for id in contents:
            ids.append(id)

    """ 중복 제거 """
    ids = list(set(ids))

    return ids

if __name__ == '__main__':
    """ E-PASS 홈페이지에서 Raw Data 긁어오기"""
    lines = get_raw_list(EPASS_URL).splitlines()
#    print(lines)

    """ Raw Data에서 ID 데이터 추출 """
    ids = get_ids(lines)
    print(ids)

    """ ID로부터 정보 가져오기 """
    for id in ids:
        url = "{}/event/new_info.asp?InNo={}".format(EPASS_URL, id)
        lines = get_raw_list(url).splitlines()
        print(lines)
