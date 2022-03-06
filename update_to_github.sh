#!/bin/bash

credential=$(cat ~/.git-credentials)

#get id from credential
id=${credential##https://}
id=${id%%:*}
echo "id : ${id}"

#get token fron credential
credential=${credential##https://${id}:}
token=${credential%%@*}
echo "token : ${token}"

body=$(cat tmp/list.html)

json="{ \"body\" : \"${body}\" }"
echo ${json} > tmp/list.json

#echo "{ \"body\" : \"${body}\" }" | \

set -x

cat tmp/list.json | \
curl \
  -u ${id}:${token} \
  -X PATCH \
  -H "Accept: application/vnd.github.v3+json" \
  --data-binary @- \
  https://api.github.com/repos/${id}/blog_automation/issues/1
