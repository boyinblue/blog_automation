#!/usr/bin/python3


def editPost(url, id, pw, post_id, post):
  print("editPost({}, {}, {})".format(url, post_id, post))
#  print("thumb :", post.thumbnail)
  url = url + "/xmlrpc.php"
#  print("id :", id)
#  print("pw :", pw)
#  print("url :", url)

  from wordpress_xmlrpc import Client
  from wordpress_xmlrpc.methods import posts

  client = Client(url, id, pw)

  client.call(posts.EditPost(post_id, post))

if __name__ == '__main__':
  from GetCredential import GetCredential
  auths = GetCredential("dhqhrtnwl")
  newPost( auths[0], auths[1], auths[2],
                  "자동 글쓰기",
                  "자동 글쓰기 테스트",
                  "자동 글쓰기 본문")
