#!/usr/bin/python3

import os

def GetCredential(page_name='mesti'):
  filename = "../.{}".format(page_name)
  if not os.path.isfile(filename):
    return None
  fp = open(filename, 'r')

  line = ' '
  while line != '':
    line = fp.readline()
    strings = line.split('\n')[0].split('=')
    if strings[0] == "URL":
      url = strings[1]
    elif strings[0] == "ID":
      id = strings[1]
    elif strings[0] == "PW":
      pw = strings[1]

  return url, id, pw

def main():
  auths = GetCredential("dhqhrtnwl")
  print("URL :", auths[0])
  print("ID :", auths[1])
  print("PW :", auths[2])

if __name__ == '__main__':
  main()
