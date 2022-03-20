import sys
import os
import pprint
import requests as req
import re
from bs4 import BeautifulSoup

blog_url="https://frankler.tistory.com"
#blog_url="https://worldclassproduct.tistory.com"

cnt = 0
urls = {}
urls2 = []
LIST_PATH = "tmp/list.html"

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

def parce_page(content, parent):
	bs = BeautifulSoup(content, 'html.parser')
	title = bs.title.string
	category_tag = bs.find('div', attrs={'class':'category'})
	if category_tag:
		category = category_tag.string
	else:
		category = ""
	a_tags = bs.findAll('a')
#	print( title )
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
			urls[href] = dict(url=full_href, title=title, category=category, parent=parent)
#			print("add url into dic : ", href)
			download_page(href, full_href)

def download_page(href, url):
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
	parce_page(file.content, href)

def make_html_report():
	p = re.compile('/[0-9]{1,}')
	for dic in urls:
		if p.match(dic):
			urls2.append(int(dic[1:]))
	urls2.sort(reverse=True)
#	print(urls2)

	f = open(LIST_PATH, 'w')
	f.write("<table>\n")
	f.write("<thead>\n")
	f.write("<tr>\n")
	f.write("<td>No</td>\n")
	f.write("<td>Title</td>\n")
	f.write("</tr>\n")
	f.write("<tr>\n")
	f.write("<td>Category</td>\n")
	f.write("<td>URL</td>\n")
	f.write("</tr>\n")
	f.write("</thead>\n")
	p = re.compile('/[0-9]{1,}')
	f.write("</tbody>\n")
	for num in urls2:
		dic = urls["/" + str(num)]
#		print(dic)
		f.write("<tr>\n")
		f.write("<td>" + str(num) + "</td>\n")
		f.write("<td>" + dic['title'] + "</td>\n")
		f.write("</tr>\n")
		f.write("<tr>\n")
		f.write("<td>" + dic['category'] + "</td>\n")
		f.write("<td>" + dic['url'] + "</td>\n")
		f.write("</tr>\n")
	f.write("</tbody>\n")
	f.write("</table>\n")
	f.close()

def main():
	# Make Directory
	if( False == os.path.isdir('tmp') ):
		os.mkdir("tmp")

	# Set RecursionLimit to avoid unexpected exit
	sys.setrecursionlimit(2000)

	# Download first page of my blog(recursive function call)
	download_page("index.html", blog_url + "/index.html")

#	Test Codes
#	urls["/84"] = dict(url="https://frankler.tistory.com/84", title="test1", parent="")
#	urls["/264"] = dict(url="https://frankler.tistory.com/264", title="test2", parent="")
#	urls["/37"] = dict(url="https://frankler.tistory.com/37", title="test3", parent="")
#	urls["?page=8"] = dict(url="https://frankler.tistory.com/?page=8", title="test4", parent="")
#	urls["?page=2"] = dict(url="https://frankler.tistory.com/?page=2", title="test5", parent="")

	# Print the dictionary with pprint
	pp = pprint.PrettyPrinter(indent=2)
	pp.pprint(urls)

	# Save only pages start with "/Number"
	# (ex) /1, /101, /301
	make_html_report()

if __name__ == "__main__":
	main()

