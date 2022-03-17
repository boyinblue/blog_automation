#!/bin/bash
set -x

credential=$(cat ~/.git-credentials)

#get id from credential
id=${credential##https://}
id=${id%%:*}
echo "id : ${id}"

#get token fron credential
credential=${credential##https://${id}:}
token=${credential%%@*}
echo "token : ${token}"

function update_issue
{
  input_file=${1}
  issue_number=${2}
  output_file=${input_file/.*/.json}

  body=$(cat ${input_file})
  body=${body//\"/\\\"}

  json="{ \"body\" : \"${body}\" }"
  echo ${json} > ${output_file}

  #echo "{ \"body\" : \"${body}\" }" | \

  cat ${output_file} | \
    curl \
    -u ${id}:${token} \
    -X PATCH \
    -H "Accept: application/vnd.github.v3+json" \
    --data-binary @- \
    https://api.github.com/repos/${id}/blog_automation/issues/${issue_number}
}

update_issue "tmp/list.html" 1
#update_issue "tmp/warning.txt" 2
