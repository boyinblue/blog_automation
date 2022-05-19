#!/usr/bin/python3

import sys
import os

sys.path.append("../wordpress")

import GetCredential
import getPosts
import getPost

auths = None
arrPost = []

def load_posts():
  global auths
  global posts

  # Get Credentials
  auths = GetCredential.GetCredential("dhqhrtnwl")

  # Get Posts
  ids = getPosts.getPosts(auths[0], auths[1], auths[2])
  for id in ids:
    post = getPost.getPost(auths[0], auths[1], auths[2], id)
    arrPost.append(post)

def check_exist(goods, period, url):
  if len(arrPost) == 0:
    load_posts()
  print("경품 :", goods)
  print("기간 :", period)
  print("URL :", url)
  for post in arrPost:
    pass

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
