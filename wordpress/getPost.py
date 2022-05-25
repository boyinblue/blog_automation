#!/usr/bin/python3

import sys

def getPost(url, id, pw, post_id):
  url = url + "/xmlrpc.php"
#  print("id :", id)
#  print("pw :", pw)
#  print("url :", url)
#  print("post id :", post_id)

  from wordpress_xmlrpc import Client
  from wordpress_xmlrpc.methods import posts

  client = Client(url, id, pw)

  post = client.call(posts.GetPost(post_id))

  return post

def print_usage():
  print("(Usage) {} -host=host -output=filename 10 20 30".format( sys.argv[0] ))

if __name__ == '__main__':
  filename = ''

  if len(sys.argv) <= 1:
    print_usage()
    exit(1)
  for i in range(1, len(sys.argv)):
    if '-host=' in sys.argv[i]:
      host = sys.argv[i][6:]
      from GetCredential import GetCredential
      auths = GetCredential(host)
    elif '-output=' in sys.argv[i]:
      filename = sys.argv[i][8:]
    else:
      if not auths:
        print("Please set host")
        print_usage()
        exit(1)

      print("Get Post", sys.argv[i])
      post = getPost(auths[0], auths[1], auths[2], sys.argv[i])

      print("id :", post.id)
      print("user :", post.user)
      print("date :", post.date)
      print("title :", post.title)
      print("slug :", post.slug)
      print("content :", post.content)
      print("[thumbnail]")
      for thumb_itr in post.thumbnail:
        print(thumb_itr)

      if filename != '':
        fp = open(filename, "w")
        fp.write(post.content)
        fp.close()
