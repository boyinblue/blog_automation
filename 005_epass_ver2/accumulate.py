#!/usr/bin/env python3

import url_preview
import re
from datetime import datetime

EPASS_URL = "https://www.e-pass.co.kr"

#p_new_data = re.compile("<a href=.*?>")
""" ID만 추출하기 위한 정규 표현식(ex : 2022-11-16-011) """
p_new_data = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{3}")

""" 이벤트 정보를 추출하기 위한 정규 표현식 """
p_meta_tag = re.compile("<meta name=\"description\" content=\".*? />")
p_title = re.compile("\"1\..*? 2\.")
p_period = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
p_product = re.compile(" 3\..*? />")

""" 이벤트 페이지를 추출하기 위한 정규 표현식 """
p_href_location = re.compile("location\.href='.*?'")

""" 순서 """
""" 1 : RAW HTML 가져오기 """
""" 2 : ID 가져오기 """
""" 3 : ID로부터 정보 가져오기 """
""" 4 : 최종 이벤트 페이지 정보 가져오기 """

def get_ids(lines):
    ids = []
    for line in lines:
        contents = p_new_data.findall(line)
        for id in contents:
            ids.append(id)

    """ 중복 제거 """
    ids = list(set(ids))

    return ids

def get_info(lines, dic):
    for line in lines:
        extracted = p_meta_tag.findall(line)
        if not extracted:
            continue
#        print(extracted)
        title = p_title.findall(line)[0][3:-3]
        period = p_period.findall(line)[0]
        product = p_product.findall(line)[0][3:-4]
        dic['title'] = title
        dic['period'] = datetime.strptime(period, "%Y-%m-%d")
        dic['product'] = product
#        print("'{}'\n'{}'\n'{}'\n".format(title, period, product))

def get_event_page(id, dic):
    url = "{}/eventinfo/get_event_url.asp".format(EPASS_URL)
    data = {"InNo" : id, "EnType": "B"}
    lines = url_preview.post_from_url(url, data).decode('euc-kr').splitlines()
    for line in lines:
#        print("Line :", line)
        event_page = p_href_location.findall(line)
        if event_page:
            event_page_url = event_page[0][14:].strip().replace('\'', '')
            print("event_page_url :", event_page_url)
            dic['url'] = event_page_url
            get_preview(event_page_url, dic)

def get_preview(url, dic):
    html = url_preview.get_text_from_url(url)
    url_preview.parse(html, dic)

def save_dictionary_to_file(id, dic):
    import pickle
    with open('tmp/' + id + '.pkl', 'wb') as f:
        pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)
    with open('tmp/' + id + '.html', 'w') as f:
        for key in dic:
            f.write("{} {}<br />\n".format(key, dic[key]))
            if key == "url":
                f.write("<a href={}>{}</a><br>\n".format(dic[key], dic['title']))
            elif key == "og:image":
                f.write("<img src={}><br />\n".format(dic[key]))

if __name__ == '__main__':
    """ E-PASS 홈페이지에서 Raw Data 긁어오기"""
    lines = url_preview.get_text_from_url(EPASS_URL).splitlines()
#    lines = get_raw_list(EPASS_URL).splitlines()
#    print(lines)

    """ Raw Data에서 ID 데이터 추출 """
    ids = get_ids(lines)
    print(ids)

    import os
    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    """ ID로부터 정보 가져오기 """
    for id in ids:
        dic = {"id": "", "url": "", "og:title": "", "og:image": "", "og:description": ""}
        import sys
        print("ID :", id)
        fp_log = open("tmp/{}.log".format(id), 'w')
        sys.stdout = fp_log
        sys.stderr = fp_log
        if os.path.exists("tmp/{}.pkl".format(id)):
            print("Skip!")
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            continue
        dic['id'] = id
        url = "{}/event/new_info.asp?InNo={}".format(EPASS_URL, id)
        lines = url_preview.get_text_from_url(url).splitlines()
        print("###########################")
        print(url)
        print("###########################")
        get_info(lines, dic)
#        print(lines)
        get_event_page(id, dic)
        dic['md'] = url_preview.make_preview(dic)
        print(dic)
        print("###########################")
        print("")

        save_dictionary_to_file(id, dic)

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
