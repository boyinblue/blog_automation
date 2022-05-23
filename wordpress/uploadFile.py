#!/usr/bin/python3

def uploadFile(url, id, pw, path):
  url = url + "/xmlrpc.php"

  from wordpress_xmlrpc import Client
  from wordpress_xmlrpc.compat import xmlrpc_client
  from wordpress_xmlrpc.methods import media

  # Get File Name From Path
  import os
  filename = os.path.basename(path)

  client = Client(url, id, pw)

  # Make dictionary In Other To Upload
  data = {'name': filename, 'type': 'image/jpg',}
  with open(path, 'rb') as img:
    data['bits'] = xmlrpc_client.Binary(img.read())
  response = client.call(media.UploadFile(data))

#  print("response :", response)

  return response

def print_usage():
  print("(Usage) {} -host=host -file=abc.jpg".format(sys.argv[0]))

if __name__ == '__main__':
  import sys 
  import os

  if len(sys.argv) == 1:
    print_usage()
    exit(1)

  for i in range(1, len(sys.argv)):
    if '-host=' in sys.argv[i]:
      host = sys.argv[i][6:]
      from GetCredential import GetCredential
      auths = GetCredential(host)
    elif '-file=' in sys.argv[i]:
      filename = sys.argv[i][6:]
      if not os.path.isfile(filename):
        print("Please set exist filename")
        print_usage()
      thumbnail = uploadFile(auths[0], auths[1], auths[2], filename)
      print("thumbnail id :", thumbnail['id'])
      print("thumbnail url :", thumbnail['url'])
    else:
      if not auths:
        print("Please set host")
        print_usage()
        exit(1)
