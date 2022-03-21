import sys
import os
import pprint
import requests as req
import re
import csv
import json

cnt = 0
urls = {}
urls2 = []
LIST_PATH = "tmp/list.html"
JSON_PATH = "tmp/list.json"

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

	global urls
	with open( JSON_PATH, 'r') as json_file:
		urls = json.load(json_file)

	# Print the dictionary with pprint
	pp = pprint.PrettyPrinter(indent=2)
	pp.pprint(urls)

	# Save only pages start with "/Number"
	# (ex) /1, /101, /301
	make_html_report()

if __name__ == "__main__":
	main()

