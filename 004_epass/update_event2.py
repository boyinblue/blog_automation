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
upload_limit = 1
upload_cnt = 0
robot_ver = 1

###############################
# 데이터 로딩 및 분석 메쏘드들 
###############################

def load_posts():
  """모든 글들을 불러와서 그 중 원하는 카테고리의 글만 리스트화 한다."""
  global arrPost

  # Get Posts
  print("모든 포스트를 불러오는 중입니다...")
  ids = getPosts.getPosts(auths[0], auths[1], auths[2])
  for id in ids:
    post = getPost.getPost(auths[0], auths[1], auths[2], id)
    if checkEventCategory(post):
      get_meta_data_from_html(post.content)
      arrPost.append(post)

def checkEventCategory(post):
  """원하는 카테고리의 글인지 체크한다."""
  for term in post.terms:
    if term.name == targetCate:
      return True
  return False

def get_posts_contain_url(event_url):
  """ 동일한 URL이 포함된 글들을 리턴한다. """
  postList = []

  for post in arrPost:
    if event_url.strip('\'') in post.content:
      postList.append(post)
      break

  return postList

def check_thumb_by_img_url(thumbnail, thumb_filename):
  """ 썸네일 이미지 URL이 썸네일에 포함되었는지 살펴본다."""

  # 썸네일의 확장자를 제거
  if thumb_filename[-4:].lower() == ".jpg":
    thumb_filename = thumb_url[0:-4]
  else:
    raise

  # 썸네일 url에 해당 파일이 포함되어있는지 살펴본다
  for thumb in thumbnail:
    if thumb_filename in thumb['link']:
      return True
  return False

def get_meta_data_from_html(content):
  """HTML 내부에 저장된 데이터를 가져온다."""
  import re

  goods = ''
  period = ''
  url = ''
  ver = ''

  lines = content.split('\n')
  for line in lines:
    found = re.findall(r' data-(.+?)=\'(.+?)\'', line)
    if len(found) == 0:
      continue
    found = found[0]
    print(found)
    id = found[0]
    data = found[1]
    if id == "goods":
      goods = data
      print("goods :", goods)
    elif id == "period":
      period = data
      print("period :", period)
    elif id == "url":
#      urls = re.findall(r'(https?://\S+)', line)
#      url = urls[0]
      url = data
      print("data-url :", url)
    elif id == "ver":
      ver = data
      print("ver :", ver)

  return {'goods':goods, "period":period, "url":url, "ver":ver}

def get_meta_data_from_txt_file(filename):
  """TXT 파일에 저장된 데이터를 가져온다."""
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

  fp.close()
  os.unlink(filename)
  return {'goods':goods, "period":period, "url":url}

def get_unique_key_from_url(url):
  return ''.join(filter(str.isalnum, url))

###############################
# 썸네일 업데이트
###############################

def upload_thumb(goods, period, url):
  """thumbnail 이미지를 생성하고 업데이트 한다."""
  """리턴값 : thumbnail 리스트 """
  import make_event_thumb

  fname = get_unique_key_from_url(url)
  fname = "{}.jpg".format(fname)
  tmp_fname = "tmp/{}".format(fname)
  print("Generate Thumb :", tmp_fname)
  make_event_thumb.draw_image(goods, period, tmp_fname)

  return uploadFile.uploadFile(auths[0], auths[1], auths[2], tmp_fname)

###############################
# 글 업데이트
###############################

def make_slug(goods, url):
  unique_key = get_unique_key_from_url(url)

  return "이벤트정보-{}-{}".format(goods, unique_key)

def update_post(post, goods, period, url, category):
  thumb = post.thumbnail
  thumb_id = None

  if len(thumb) == 0:
    print("Make thumb")
    thumb = upload_thumb(goods, period, url)
    thumb_id = thumb['id']
  img_url = thumb['link']

  title = "[이벤트 정보] {} ({})".format(goods, period)
  slug = make_slug(goods, url)
  if img_url == '':
    img_tag = ""
  else:
    img_tag = "<img src={}><br>\n".format(img_url)
  title_tag = "<h2>이벤트 정보</h2>\n"
  goods_tag = "<p data-goods='{}'>상품 : {}</p>\n".format(goods, goods)
  period_tag = "<p data-period='{}'>이벤트 기간 : {}</p>\n".format(period, period)
  link_tag = '<p data-ke-size="size16"><a data-url="{}" style="background-color: #0040ff; color: #fff; border-radius: 30px; padding: 16px 32px; font-size: 20px; font-weight: bold; text-decoration: none;" href={}>이벤트 바로가기</a></p>'.format(url, url)
  robot_tag = '<p data-version={}> </p>'.format(robot_ver)

  content = "{}{}{}{}{}".format(title_tag,
          goods_tag,
          period_tag,
          link_tag,
          robot_tag)

  import editPost
  post.title = title
  post.content = content
  if thumb_id:
    post.thumbnail=thumb['id']
  if category:
    post.term=category
  post.post_status = 'publish'
  editPost.editPost( auths[0], auths[1], auths[2], post.id, post)

###############################
# 새로운 이벤트 데이터를 생성
###############################

def add_post_by_dir(dir):
  """디렉토리를 순회하면서 이벤트 파일을 살펴본다."""

  global upload_cnt

  print("load event data by dir ({})".format(dir))
  dirs = os.listdir(dir)
  for dirname in dirs:
    if not os.path.isdir("{}/{}".format(dir,dirname)):
      continue
    elif not os.path.isfile("{}/{}/data.txt".format(dir,dirname)):
      continue
    elif upload_cnt >= upload_limit:
      return 

    if add_post_by_file("{}/{}/data.txt".format(dir,dirname)):
      upload_cnt = upload_cnt + 1

def add_post_by_file(filename):
  global upload_cnt

  print("")
  print("load event data by file:", filename)
  data = get_meta_data_from_txt_file(filename)

  postList = get_posts_contain_url(data['url'])
  if len(postList) == 0:
    print("[AUTO] Add Post : {} / {} / {}".format(data['goods'],
            data['period'], data['url']))
    post_id = new_post(data)
    post = getPost.getPost(auths[0], auths[1], auths[2], post_id)
    update_post(post, data['goods'], data['period'],
                    data['url'], targetCate)
    upload_cnt = upload_cnt + 1
    
def new_post(data):
  import newPost
  slug = make_slug(data['goods'], data['url'])
  post = newPost.newPost( auths[0], auths[1], auths[2],
                  slug = slug, category = targetTerm )
  return post

###############################
# 등록된 글 관리
###############################

def manage_post():
  for post in arrPost:
    pass

    ### 이벤트 기간이 지났을 경우

    ### 버전이 맞지 않을 경우
#    edit_post(post, goods, period, url, targetCate)

###############################
# 메인 함수 및 사용법 안내
###############################
def print_usage():
  print("[ How To Add Event Data ]")
  print("{} -host=hostname -op=add -dir=tmp".format(sys.argv[0]))
  print("")
  print("[ How To Manage Posts ]")
  print("{} -host=hostname -op=manage".format(sys.argv[0]))

def main():
  op = None

  for i in range(1, len(sys.argv)):
    if '-host=' in sys.argv[i]:
      global host
      host = sys.argv[i][6:]
    elif '-dir=' in sys.argv[i]:
      global path
      path = sys.argv[i][5:]
    elif '-op=' in sys.argv[i]:
      op = sys.argv[i][4:]

  if not host:
    print("Please set host")
    print_usage()
    exit(2)

  global auths
  auths = GetCredential.GetCredential(host)

  # Get Term
  global targetTerm
  targetTerm = getTaxonomies.getTermByName(
                  auths[0], auths[1], auths[2], targetCate)

  if op == "add":
    if not path:
      print("Please set directory")
      print_usage()
      exit(3)
    elif not os.path.isdir(path):
      print("Cannot find dir :", path)
      exit(4)
    # Load Posts
    load_posts()
    add_post_by_dir(path)
  elif op == "manage":
    # Check directory to upload
    # Load Posts
    load_posts()
    manage_post()
  else:
    print("Please check operation :", op)
    print_usage()

if __name__ == '__main__':
  main()
