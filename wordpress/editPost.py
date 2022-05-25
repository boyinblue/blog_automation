#!/usr/bin/python3

import sys

def editPost(url, id, pw, post_id, post):
  print("editPost({}, {}, {})".format(url, post_id, post))
#  print("thumb :", post.thumbnail)
  url = url + "/xmlrpc.php"
#  print("id :", id)
#  print("pw :", pw)
#  print("url :", url)

  from wordpress_xmlrpc import Client
  from wordpress_xmlrpc.methods import posts

  client = Client(url, id, pw)

  client.call(posts.EditPost(post_id, post))

def print_usage():
  print("{} -host=host -file=filename -post_id=6".format(sys.argv[0]))

if __name__ == '__main__':
  content = ''
  auths = []
  post_id = 0

  for i in range(1, len(sys.argv)):
    if '-host=' in sys.argv[i]:
      host = sys.argv[i][6:]

      from GetCredential import GetCredential
      auths = GetCredential(host)
    elif '-file=' in sys.argv[i]:
      file = sys.argv[i][5:]
      fp = open(file, "r")
      content = fp.readlines()
      fp.close()
    elif '-post_id=' in sys.argv[i]:
      post_id = sys.argv[i][9:]

  if len(auths) == 0:
    print("Please check credential info")
    print_usage()
    exit(1)
  elif post_id == 0:
    print("Please check post ID")
    print_usage()
    exit(2)

  import getPost
  post = getPost.getPost( auths[0], auths[1], auths[2], post_id)
  post.content = content
  editPost( auths[0], auths[1], auths[2], post_id, post )
