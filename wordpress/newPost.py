#!/usr/bin/python3

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts

def newPost(url, id, pw, title, slug, content):
  print("id :", id)
  print("pw :", pw)
  url = url + "/xmlrpc.php"
  print("url :", url)
  client = Client(url, id, pw)
  post = WordPressPost()
  post.title = title
  post.slug = slug
  post.content = content
  post.terms_names = {
                  'post_tag': 'wordpress',
                  'category' : ['']
  }

  post.post_status = 'publish'
  client.call(posts.NewPost(post))

if __name__ == '__main__':
  newPost( "https://www.dhqhrtnwl.shop",
                  'esregnet0409@gmail.com',
                  'honor0904',
                  "자동 글쓰기",
                  "자동 글쓰기 테스트",
                  "자동 글쓰기 본문")
