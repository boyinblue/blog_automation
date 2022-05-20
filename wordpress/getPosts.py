#!/usr/bin/python3

def getPosts(a, b, c):
  print(a, b, c)

def getPosts(url, id, pw):
  url = url + "/xmlrpc.php"
#  print("id :", id)
#  print("pw :", pw)
#  print("url :", url)

  from wordpress_xmlrpc import Client
  from wordpress_xmlrpc.methods import posts

  client = Client(url, id, pw)

  ids = []
  offset = 0
  increment = 20

  while True:
    postList = client.call(posts.GetPosts({'number':increment,'offset':offset}))
    if len(postList) == 0:
      break
    for post in postList:
      ids.append(post.id)
    offset = offset + increment

  return ids

if __name__ == '__main__':
  from GetCredential import GetCredential

#  auths = GetCredential('mesti')
  auths = GetCredential('dhqhrtnwl')
  ids = getPosts(auths[0], auths[1], auths[2])
  print("Posts :", ids)
