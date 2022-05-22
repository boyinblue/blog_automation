#!/usr/bin/python3

import sys
import os

sys.path.append("../wordpress")

import GetCredential
import getPosts
import getPost
import newPost
import getTaxonomies

host = None
auths = None
path = None
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
  print("모든 포스트를 불러오는 중입니다...")
  ids = getPosts.getPosts(auths[0], auths[1], auths[2])
  for id in ids:
    post = getPost.getPost(auths[0], auths[1], auths[2], id)
    if checkEventCategory(post):
      arrPost.append(post)

def upload_file(tmp_fname, fname):
  import paramiko
  from scp import SCPClient, SCPException

  ssh = GetCredential.GetSsh(host)

  ssh_client = paramiko.SSHClient()
  ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh_client.connect(ssh[0], username=ssh[1], password=ssh[2])

  remote_path = "/var/www/wordpress/wp-content/custom/event_info"
  url = "/wp-content/custom/event_info/{}".format(fname)

  try:
    with SCPClient(ssh_client.get_transport()) as scp:
      scp.put(tmp_fname, remote_path, preserve_times=True)
  except SCPException:
    print("SCP 업로드에 실패하였습니다.")
    print("Remote Path :", remote_path)
    url = ''

  ssh_client.close()

  return url

def upload_thumb(goods, period, url):
  import make_event_thumb

  fname = ''.join(filter(str.isalnum, url)) 
  fname = "{}.jpg".format(fname)
  tmp_fname = "tmp/{}".format(fname)
  print("Generate Thumb :", tmp_fname)
  make_event_thumb.draw_image(goods, period, tmp_fname)

  return upload_file(tmp_fname, fname)

def write_post(post_id, goods, period, url, category, post=None):
  img_url = upload_thumb(goods, period, url)
  title = "[이벤트 정보] {} ({})".format(goods, period)
  slug = "이벤트정보-{}".format(goods)
  if img_url == '':
    img_tag = ""
  else:
    img_tag = "<img src={}><br>\n".format(img_url)
  link = '<p data-ke-size="size16"><a style="background-color: #0040ff; color: #fff; border-radius: 30px; padding: 16px 32px; font-size: 20px; font-weight: bold; text-decoration: none;" href={}>이벤트 바로가기</a></p>'.format(url)
  content = "{}\n\
             <h2>이벤트 정보</h2>\n\
             상품 : {}<br>\n\
             이벤트 기간 : {}<br>\n\
             {}\n".format(
                             img_tag, goods, period, link)
  if post_id == 0:
    newPost.newPost( auths[0], auths[1], auths[2],
        title, slug, content, targetTerm)
  elif not post:
    raise
  else:
    import editPost
    post.content = content
    editPost.editPost( auths[0], auths[1], auths[2], post_id, post)

def check_exist(goods, period, url):
  post_id = 0
  print("경품 :", goods)
  print("기간 :", period)
  print("URL :", url)
  for post in arrPost:
    if url.strip('\'') in post.content:
      print("{}에 포함".format(post.title))
      post_id = post.id
      break

  if post_id == 0:
    print("[AUTO] Write Post : {} / {} / {}".format(goods, period, url))
    write_post(post_id, goods, period, url, targetCate)
  else:
    print("[AUTO] Edit Post : {} / {} / {}".format(goods, period, url))
    write_post(post_id, goods, period, url, targetCate, post=post)

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
      event_period = strings[1]
    elif strings[0] == "경품":
      event_goods = strings[1]
    elif strings[0] == "링크":
      event_url = strings[1]
  check_exist(event_goods, event_period, event_url)

def main():
  import sys
  for i in range(1, len(sys.argv)):
    if '-host=' in sys.argv[i]:
      global host
      host = sys.argv[i][6:]
    elif '-dir=' in sys.argv[i]:
      global path
      path = sys.argv[i][5:]

  if not host:
    print("Please set host")
    print("{} -host=hostname".format(sys.argv[0]))
    exit(2)

  global auths
  auths = GetCredential.GetCredential(host)

  # Get Term
  global targetTerm
  targetTerm = getTaxonomies.getTermByName(
                  auths[0], auths[1], auths[2], targetCate)

  # Load Posts
  load_posts()

  if not path:
    print("Please set directory")
    print("{} -dir=tmp".format(sys.argv[0]))
    exit(3)
  elif not os.path.isdir(path):
    print("Cannot find dir :", path)
    exit(4)
  search_event_data(path)

if __name__ == '__main__':
  main()
