#!/usr/bin/python3

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts

def getPosts(url, id, pw):
  print("id :", id)
  print("pw :", pw)
  url = url + "/xmlrpc.php"
  print("url :", url)
  client = Client(url, id, pw)

  postList = client.call(posts.GetPosts())
  for post in postList:
    print("ID :", post.id)

if __name__ == '__main__':
  getPosts( "https://www.dhqhrtnwl.shop",
                  'esregnet0409@gmail.com',
                  'honor0904')
