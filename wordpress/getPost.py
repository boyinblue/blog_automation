#!/usr/bin/python3

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

if __name__ == '__main__':
  import sys 
  for i in range(1, len(sys.argv)):
    if '-host=' in sys.argv[i]:
      host = sys.argv[i][6:]
      from GetCredential import GetCredential
      auths = GetCredential(host)
    else:
      if not auths:
        print("Please set host")
        print("(Usage) {} -host=dhqhrtnwl 10 20 30".format(sys.argv[0]))
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
