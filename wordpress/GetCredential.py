#!/usr/bin/python3

import os

def GetCredential(page_name='mesti'):
  filename = "../.{}".format(page_name)
  if not os.path.isfile(filename):
    print("There is not file on", filename)
    raise
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

def GetSsh(page_name='mesti'):
  filename = "../.{}".format(page_name)
  if not os.path.isfile(filename):
    return None
  fp = open(filename, 'r')

  line = ' '
  while line != '':
    line = fp.readline()
    strings = line.split('\n')[0].split('=')
    if strings[0] == "SSH_HOST":
      hostname = strings[1]
    elif strings[0] == "SSH_ID":
      id = strings[1]
    elif strings[0] == "SSH_PW":
      pw = strings[1]

  return hostname, id, pw

def main():
  auths = GetCredential("dhqhrtnwl")
  print("URL :", auths[0])
  print("ID :", auths[1])
  print("PW :", auths[2])

  ssh = GetSsh("dhqhrtnwl")
  print("Hostname :", ssh[0])
  print("ID :", ssh[1])
  print("PW :", ssh[2])

if __name__ == '__main__':
  main()
