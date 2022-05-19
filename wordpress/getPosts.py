#!/usr/bin/python3

from GetCredential import GetCredential

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts

def getPosts(url, id, pw):
  print("id :", id)
  print("pw :", pw)
  url = url + "/xmlrpc.php"
  print("url :", url)

  client = Client(url, id, pw)

  ids = []

  postList = client.call(posts.GetPosts())
  for post in postList:
    print("ID :", post.id)
    ids.append(post.id)

  return ids

if __name__ == '__main__':
#  auths = GetCredential('mesti')
  auths = GetCredential('dhqhrtnwl')
  getPosts(auths[0], auths[1], auths[2])
