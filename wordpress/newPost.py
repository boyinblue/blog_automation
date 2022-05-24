#!/usr/bin/python3


def newPost(url, id, pw, title, slug, content, category=None, thumb=None):
  url = url + "/xmlrpc.php"
#  print("id :", id)
#  print("pw :", pw)
#  print("url :", url)

  from wordpress_xmlrpc import Client, WordPressPost
  from wordpress_xmlrpc.methods import posts

  client = Client(url, id, pw)

  post = WordPressPost()
  post.title = title
  post.slug = slug
  post.content = content
  if category:
#    print("terms :", post.terms)
    post.terms.append(category)
  if thumb:
    post.thumbnail = thumb

  post.post_status = 'publish'
  client.call(posts.NewPost(post))

if __name__ == '__main__':
  from GetCredential import GetCredential
  auths = GetCredential("dhqhrtnwl")
  newPost( auths[0], auths[1], auths[2],
                  "자동 글쓰기",
                  "자동 글쓰기 테스트",
                  "자동 글쓰기 본문")
