#!/usr/bin/python3

from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts

def getPosts(url, id, pw):
  url = url + "/xmlrpc.php"
#  print("id :", id)
#  print("pw :", pw)
#  print("url :", url)

  client = Client(url, id, pw)

  ids = []

  postList = client.call(posts.GetPosts())
  for post in postList:
#    print("ID :", post.id)
    ids.append(post.id)

  return ids

if __name__ == '__main__':
  from GetCredential import GetCredential

#  auths = GetCredential('mesti')
  auths = GetCredential('dhqhrtnwl')
  ids = getPosts(auths[0], auths[1], auths[2])
  print("Posts :", ids)
