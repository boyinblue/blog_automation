import sys
import os
import pprint
import requests as req
import re
import csv
import json
from bs4 import BeautifulSoup

blog_url="https://frankler.tistory.com"
#blog_url="https://worldclassproduct.tistory.com"

cnt = 0
urls = {}
urls2 = []
JSON_PATH = "tmp/list.json"
CSV_PATH = "tmp/list.csv"

for i in range( 1, len(sys.argv) ):
    print("[ARG] " + sys.argv[i])
    if "-json=" in sys.argv[i]:
        JSON_PATH = sys.argv[i][6:]
    elif "-csv=" in sys.argv[i]:
        CSV_PATH = sys.argv[i][5:]

skip_keyword_contain = \
{ \
    "category=",
    "#comment",
    "#page-more"
}

skip_keyword_start = \
{ \
    "http://",
    "https://",
    "/tag",
    "/category",
    "/auth",
    "/toolbar",
#    "/entry",
    "javascript:",
    "#content"
}

skip_keyword_equal = \
{ \
    "/"
}

def check_skip_keyword(line):
    for keyword in skip_keyword_contain:
        if keyword in line:
            return True
    for keyword in skip_keyword_start:
        if line.startswith(keyword):
            return True
    for keyword in skip_keyword_equal:
        if keyword == line:
            return True
    return False

def parce_page(content, parent, url):
	print("parce", parent, url)
	bs = BeautifulSoup(content, 'html.parser')

	title = bs.title.string
	urls[parent]['title'] = title

	category_tag = bs.find('div', attrs={'class':'category'})
	if category_tag:
		category = category_tag.string
	else:
		category = ""
	urls[parent]['category'] = category

	a_tags = bs.findAll('a')
	for tag in a_tags:
#		print(tag.attrs)
		if 'href' in tag.attrs:
			href = tag.attrs['href']
			if check_skip_keyword(href):
				continue
			elif href in urls:
				continue

			if href[0:1] == "/":
				full_href=blog_url + href
			else:
				full_href=blog_url + "/" + href
#			print("add url into dic : ", href)
			download_page(href, full_href, parent)

def download_page(href, url, parent):
	global cnt
	cnt = cnt + 1
	print("===================")
	print(str(cnt) + " : " + url)
	print("===================")
	print("")
#	if( cnt > 10 ):
#		return
	file = req.get(url)
#	print(file.content)
	urls[href] = dict(url=url, title='', category='', parent=parent)
	parce_page(file.content, href, url)

def main():
	# Make Directory
	if( False == os.path.isdir('tmp') ):
		os.mkdir("tmp")

	# Set RecursionLimit to avoid unexpected exit
	sys.setrecursionlimit(2000)

	# Download first page of my blog(recursive function call)
	download_page("index.html", blog_url + "/index.html", "/")

	# Print the dictionary with pprint
	pp = pprint.PrettyPrinter(indent=2)
	pp.pprint(urls)

    # Save dictionary with csv format
	with open( CSV_PATH, 'w') as f:
		w = csv.writer(f)
		for key in urls.keys():
#			w.writerow(key)
			w.writerow(urls[key].values())

	# Save dictionary with json format
	with open( JSON_PATH, 'w') as fp:
		json.dump(urls, fp)

if __name__ == "__main__":
	main()

