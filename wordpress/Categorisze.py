#!/usr/bin/python3

import sys
import os
import GetCredential
import getPosts
import getPost
import editPost
import getTaxonomies

auths = None
arrPost = []
target = None

def categorize(post):
  unTerm = None
  categorized = False

  print("Check Category :", post.title)

  for term in post.terms:
    if term.taxonomy != 'category':
      continue
    print("Cate :", term.id, term.group, term.taxonomy, term.taxonomy_id)
    if term.name == '미분류':
      unTerm = term
    else:
      categorized = True

  if unTerm and categorized:
    post.terms.remove(unTerm)
    print("editPost({}, {})".format(post.id, post.title))
    editPost.editPost(auths[0], auths[1], auths[2], post.id, post)

def load_posts():
  global arrPost

  # Get Posts
  ids = getPosts.getPosts(auths[0], auths[1], auths[2])
  for id in ids:
    post = getPost.getPost(auths[0], auths[1], auths[2], id)
    categorize(post)

def print_usage():
  print("(Usage) {} -target=dhqhrtnwl".format(sys.argv[0]))

def main():
  global target

  for i in range(1, len(sys.argv)):
    if '-target=' in sys.argv[i]:
      target = sys.argv[i][8:]
      print("Target =", target)

  if not target:
    print("Please set target")
    print_usage()
    exit(1)

  # Get Credentials
  global auths
  auths = GetCredential.GetCredential(target)

  load_posts()

if __name__ == '__main__':
  main()
