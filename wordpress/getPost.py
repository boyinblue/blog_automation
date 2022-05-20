#!/usr/bin/python3

from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts

def getPost(url, id, pw, post_id):
  url = url + "/xmlrpc.php"
#  print("id :", id)
#  print("pw :", pw)
#  print("url :", url)
#  print("post id :", post_id)

  client = Client(url, id, pw)

  post = client.call(posts.GetPost(post_id))


  return post

if __name__ == '__main__':
  from GetCredential import GetCredential
  auths = GetCredential('dhqhrtnwl')

  import sys
  if len(sys.argv) <= 1:
    print("Please input specific post id")
    exit(0)

  for i in range(1, len(sys.argv)):
    print("Get Post", sys.argv[i])
    post = getPost(auths[0], auths[1], auths[2], sys.argv[i])

    print("id :", post.id)
    print("user :", post.user)
    print("date :", post.date)
    print("title :", post.title)
    print("slug :", post.slug)
