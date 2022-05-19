#!/usr/bin/python3
import os

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts

def getPost(url, id, pw):
  print("id :", id)
  print("pw :", pw)
  url = url + "/xmlrpc.php"
  print("url :", url)
  client = Client(url, id, pw)

  post = WordPressPost()
  post.post_id = 6
  post = client.call(posts.GetPost(post))

  print("id :", post.id)
  print("user :", post.user)
  print("date :", post.date)

if __name__ == '__main__':
  getPost( "https://www.dhqhrtnwl.shop",
                  'esregnet0409@gmail.com',
                  'honor0904')
