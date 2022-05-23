#!/usr/bin/python3

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
  import sys 
  for i in range(1, len(sys.argv)):
    if '-host=' in sys.argv[i]:
      host = sys.argv[i][6:]

  if not host:
    print("Please set host")
    print("(Usage) {} -host=dhqhrtnwl".format(host))
    exit(1)

  from GetCredential import GetCredential
  auths = GetCredential(host)

  ids = getPosts(auths[0], auths[1], auths[2])
  print("Posts :", ids)
