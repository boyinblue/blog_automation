#!/usr/bin/python3

def newPost(url, id, pw, title = None, slug = None, content = None, category=None, thumb=None):
  url = url + "/xmlrpc.php"
#  print("id :", id)
#  print("pw :", pw)
#  print("url :", url)

  from wordpress_xmlrpc import Client, WordPressPost
  from wordpress_xmlrpc.methods import posts

  client = Client(url, id, pw)

  post = WordPressPost()
  if title:          
    post.title = title
  if slug:
    post.slug = slug
  if content:
    post.content = content
  if category:
#    print("terms :", post.terms)
    post.terms.append(category)
  if thumb:
    post.thumbnail = thumb

  return client.call(posts.NewPost(post))

if __name__ == '__main__':
  from GetCredential import GetCredential
  auths = GetCredential("dhqhrtnwl")
  newPost( auths[0], auths[1], auths[2],
                  "자동 글쓰기",
                  "자동 글쓰기 테스트",
                  "자동 글쓰기 본문")
