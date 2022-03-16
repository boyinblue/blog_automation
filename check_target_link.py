import sys
import os
import pprint
import requests as req
from bs4 import BeautifulSoup

blog_url="https://frankler.tistory.com"

urls={}

def parce_page(content, parent):
	bs = BeautifulSoup(content, 'html.parser')
	tags = bs.findAll('a')
	title = bs.title
	for tag in tags:
#		print(tag.attrs)
		if 'href' in tag.attrs:
			href=tag.attrs['href']
			if href in urls:
				continue
			elif href.startswith("http://"):
				continue
			elif href.startswith("https://"):
				continue
			elif href == "/":
				continue
			elif href.startswith("/tag"):
				continue
			elif href.startswith("/category"):
				continue
			elif href.startswith("/auth"):
				continue
			elif href.startswith("/toolbar"):
				continue
			elif href.startswith("javascript:"):
				continue
			elif "category=" in href:
				continue
			elif "#comment" in href:
				continue
#			elif href[0:1] == "#":
#				continue

			if href[0:1] == "/":
				full_href=blog_url + href
			else:
				full_href=blog_url + "/" + href
			urls[href] = dict(url=full_href, title=title, parent=parent)
			download_page(href, full_href)

def download_page(href, url):
	print("===================")
	print(url)
	print("===================")
	print("")
	file = req.get(url)
#	print(file.content)
	parce_page(file.content, href)

sys.setrecursionlimit(2000)

download_page("index.html", blog_url + "/index.html")

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(urls)
