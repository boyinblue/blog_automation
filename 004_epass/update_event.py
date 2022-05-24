#!/usr/bin/python3

import sys
import os

sys.path.append("../wordpress")

import GetCredential
import getPosts
import getPost
import getTaxonomies
import uploadFile

# 인증 관련 전역 변수
host = None
auths = None
path = None

# 글 관련 전역 변수
arrPost = []
targetCate = "이벤트 정보"
targetTerm = None

# 동작 관련 전역 변수
op = 'both'   # add, edit, both
upload_limit = 1
upload_cnt = 0

def checkEventCategory(post):
  "원하는 카테고리의 글인지 체크한다."
  for term in post.terms:
    if term.name == targetCate:
      return True
  return False

def load_posts():
  "모든 글들을 불러와서 그 중 원하는 카테고리의 글만 리스트화 한다."
  global arrPost

  # Get Posts
  print("모든 포스트를 불러오는 중입니다...")
  ids = getPosts.getPosts(auths[0], auths[1], auths[2])
  for id in ids:
    post = getPost.getPost(auths[0], auths[1], auths[2], id)
    if checkEventCategory(post):
      arrPost.append(post)

def upload_thumb(goods, period, url):
  """thumbnail 이미지를 생성하고 업데이트 한다."""
  """리턴값 : thumbnail 리스트 """
  import make_event_thumb

  fname = ''.join(filter(str.isalnum, url)) 
  fname = "{}.jpg".format(fname)
  tmp_fname = "tmp/{}".format(fname)
  print("Generate Thumb :", tmp_fname)
  make_event_thumb.draw_image(goods, period, tmp_fname)

  return uploadFile.uploadFile(auths[0], auths[1], auths[2], tmp_fname)

def new_post():
  import newPost
  post = newPost.newPost( auths[0], auths[1], auths[2] )
  return post

def edit_post(post, goods, period, url, category):
  thumb = post.thumbnail
  thumb_id = None

  if len(thumb) == 0:
    print("Make thumb")
    thumb = upload_thumb(goods, period, url)
    thumb_id = thumb['id']
  img_url = thumb['link']

  title = "[이벤트 정보] {} ({})".format(goods, period)
  slug = "이벤트정보-{}".format(goods)
  if img_url == '':
    img_tag = ""
  else:
    img_tag = "<img src={}><br>\n".format(img_url)
  title_tag = "<h2>이벤트 정보</h2>\n"
  goods_tag = "<p data-goods='{}'>상품 : {}</p>\n".format(goods, goods)
  period_tag = "<p data-period='{}'>이벤트 기간 : {}</p>\n".format(period, period)
  link_tag = '<p data-ke-size="size16"><a data-url="{}" style="background-color: #0040ff; color: #fff; border-radius: 30px; padding: 16px 32px; font-size: 20px; font-weight: bold; text-decoration: none;" href={}>이벤트 바로가기</a></p>'.format(url, url)
  content = "{}{}{}{}{}".format(img_tag, title_tag, goods_tag, period_tag, link_tag)

  import editPost
  post.content = content
  if thumb_id:
    post.thumbnail=thumb['id']
  post.post_status = 'publish'
  editPost.editPost( auths[0], auths[1], auths[2], post.id, post)

def check_exist(url):
  """ 동일한 URL이 포함된 글이 있는지 살펴본다. """
  postList = []

  for post in arrPost:
    if url.strip('\'') in post.content:
      postList.append(post)
      break

  return postList

def search_event_data(dir):
  print("search event data at ({})".format(dir))
  filenames = os.listdir(dir)
  for filename in filenames:
#    print("filename :", filename)
    if filename[-4:].lower() == ".txt":
      print("")
      print("load event data :", filename)
      load_event_data("{}/{}".format(dir,filename))

def load_event_data(filename):
  fp = open(filename, 'r')
  line = ' '
  while line != '':
    line = fp.readline()
    strings = line.split('\n')[0].split('|')
    if strings[0] == "응모기간":
      period = strings[1]
    elif strings[0] == "경품":
      goods = strings[1]
    elif strings[0] == "링크":
      url = strings[1]

  postList = check_exist(url)
  if len(postList) > 0:
    if len(postList) > 1:
      print("Posts are duplicated!")
    for post in postList:
      if op == 'edit' or op == 'both':
        print("[AUTO] Edit Post : {} / {} / {} / {}".format(post.id, goods, period, url))
        edit_post(post, goods, period, url, targetCate)
  else:
    if op != 'add' and op != 'both' and upload_cnt > upload_limit:
      return 
    print("[AUTO] Add Post : {} / {} / {}".format(goods, period, url))
    post_id = new_post()
    post = getPost.getPost(auths[0], auths[1], auths[2], post_id)
    edit_post(post, goods, period, url, targetCate)

def print_usage():
  print("{} -host=hostname -dir=tmp".format(sys.argv[0]))

def main():
  for i in range(1, len(sys.argv)):
    if '-host=' in sys.argv[i]:
      global host
      host = sys.argv[i][6:]
    elif '-dir=' in sys.argv[i]:
      global path
      path = sys.argv[i][5:]
    elif '-op=' in sys.argv[i]:
      global op
      op = sys.argv[i][4:]

  if not host:
    print("Please set host")
    print_usage()
    exit(2)
  elif not path:
    print("Please set directory")
    print_usage()
    exit(3)
  elif not os.path.isdir(path):
    print("Cannot find dir :", path)
    exit(4)

  global auths
  auths = GetCredential.GetCredential(host)

  # Get Term
  global targetTerm
  targetTerm = getTaxonomies.getTermByName(
                  auths[0], auths[1], auths[2], targetCate)

  # Load Posts
  load_posts()

  # Check directory to upload
  search_event_data(path)

if __name__ == '__main__':
  main()
