#!/usr/bin/python3

from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import taxonomies

def getTaxonomies(url, id, pw):
  client = Client(url + "/xmlrpc.php", id, pw)
  taxoList = client.call(taxonomies.GetTaxonomies())
  return taxoList

def getTerms(url, id, pw, taxoName):
  client = Client(url + "/xmlrpc.php", id, pw)
  termList = client.call(taxonomies.GetTerms(taxoName))
  return termList

def getCateIdByName(url, id, pw, cateName):
  term = getTermByName(url, id, pw, cateName)
  if term:
    return term.id
  return None

def getTermByName(url, id, pw, cateName):
  client = Client(url + "/xmlrpc.php", id, pw)
  termList = client.call(taxonomies.GetTerms('category'))
  for term in termList:
    if cateName == term.name:
      return term
  return None
    
if __name__ == '__main__':
  from GetCredential import GetCredential
  auths = GetCredential('dhqhrtnwl')

  taxoList = getTaxonomies(auths[0], auths[1], auths[2])
  for taxo in taxoList:
    print("name :", taxo.name)
    print("label :", taxo.label)

    termList = getTerms(auths[0], auths[1], auths[2], taxo.name)
    for term in termList:
      print("  id :", term.id)
      print("  name :", term.name)

  print("이벤트 정보 카테고리 ID :",
                  getCateIdByName(auths[0],
                          auths[1], auths[2], "이벤트 정보"))
