#!/bin/bash

id="boyinblue"
body=$(cat tmp/list.html)
token="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"

json="{ \"body\" : \"${body}\" }"
echo ${json} > tmp/list.json

#echo "{ \"body\" : \"${body}\" }" | \
cat tmp/list.json | \
curl \
  -u ${id}:${token} \
  -X PATCH \
  -H "Accept: application/vnd.github.v3+json" \
  --data-binary @- \
  https://api.github.com/repos/${id}/blog_automation/issues/1
