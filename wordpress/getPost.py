#!/usr/bin/python3
import os

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts

def getPost(url, id, pw, post_id):
  url = url + "/xmlrpc.php"

  client = Client(url, id, pw)

  post = client.call(posts.GetPost(post_id))

  return post

  return post

if __name__ == '__main__':
  getPost( "https://www.dhqhrtnwl.shop",
                  'esregnet0409@gmail.com',
                  'honor0904')
