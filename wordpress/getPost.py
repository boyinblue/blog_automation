#!/usr/bin/python3
import os

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts

def getPost(url, id, pw, post_id):
  url = url + "/xmlrpc.php"
#  print("id :", id)
#  print("pw :", pw)
#  print("url :", url)
#  print("post id :", post_id)

  client = Client(url, id, pw)

  post = client.call(posts.GetPost(post_id))

#  print("id :", post.id)
#  print("user :", post.user)
#  print("date :", post.date)
#  print("title :", post.title)
#  print("slug :", post.slug)

if __name__ == '__main__':
  getPost( "https://www.dhqhrtnwl.shop",
                  'esregnet0409@gmail.com',
                  'honor0904')
