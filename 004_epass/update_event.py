#!/usr/bin/python3

import sys
import os

sys.path.append("../wordpress")

import GetCredential
import getPosts
import getPost
import newPost
import getTaxonomies

auths = None
arrPost = []
targetCate = "이벤트 정보"
targetTerm = None

def checkEventCategory(post):
  for term in post.terms:
    if term.name == targetCate:
      return True
  return False

def load_posts():
  global arrPost

  # Get Posts
  ids = getPosts.getPosts(auths[0], auths[1], auths[2])
  for id in ids:
    post = getPost.getPost(auths[0], auths[1], auths[2], id)
    if checkEventCategory(post):
      arrPost.append(post)

def write_post(goods, period, url, category):
  title = "[이벤트 정보] {} ({})".format(goods, period)
  slug = "이벤트정보-{}".format(goods)
  link = '<p data-ke-size="size16"><a style="background-color: #0040ff; color: #fff; border-radius: 30px; padding: 16px 32px; font-size: 20px; font-weight: bold; text-decoration: none;" href={}>더보기</a></p>'.format(url)
  content = "<h2>이벤트 정보</h2>\n\
                  상품 : {}<br>\n\
                  이벤트 기간 : {}<br>\n\
                  {}\n".format(
                                  goods, period, link)
  newPost.newPost( auths[0], auths[1], auths[2],
        title, slug, content, targetTerm)

def check_exist(goods, period, url):
  if len(arrPost) == 0:
    load_posts()
  print("경품 :", goods)
  print("기간 :", period)
  print("URL :", url)
  for post in arrPost:
    if url.strip('\'') in post.content:
      print("{}에 포함".format(post.title))
      return True
#    else:
#      print("{} 못찾음 {}".format(url.strip('\''), post.content))

  print("[AUTO] Write Post : {} / {} / {}".format(goods, period, url))
  write_post(goods, period, url, targetCate)

def search_event_data(dir):
  print("search event data at ({})".format(dir))
  filenames = os.listdir(dir)
  for filename in filenames:
#    print("filename :", filename)
    if filename[-4:].lower() == ".txt":
      print("load event data :", filename)
      load_event_data("{}/{}".format(dir,filename))

def load_event_data(filename):
  fp = open(filename, 'r')
  line = ' '
  while line != '':
    line = fp.readline()
    strings = line.split('\n')[0].split('|')
    if strings[0] == "응모기간":
      event_period = strings[1]
    elif strings[0] == "경품":
      event_goods = strings[1]
    elif strings[0] == "링크":
      event_url = strings[1]
  check_exist(event_goods, event_period, event_url)

def main():
  # Get Credentials
  global auths
  auths = GetCredential.GetCredential("dhqhrtnwl")

  # Get Term
  global targetTerm
  targetTerm = getTaxonomies.getTermByName(
                  auths[0], auths[1], auths[2], targetCate)

  if len(sys.argv) > 3:
    event_goods = sys.argv[1]
    event_period = sys.argv[2]
    event_url = sys.argv[3]
    check_exist(event_goods, event_period, event_url)
  elif len(sys.argv) > 1:
    path = sys.argv[1]
    if not os.path.isdir(path):
      print("Cannot find file :", path)
      exit(0)
    search_event_data(path)
  else:
    print("There is no parameter")

if __name__ == '__main__':
  main()
