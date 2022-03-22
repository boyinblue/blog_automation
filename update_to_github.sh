#!/bin/bash
set -x

credential=$(cat ~/.git-credentials)

output_file="tmp/issue_update.json"

#get id from credential
id=${credential##https://}
id=${id%%:*}
echo "id : ${id}"

#get token fron credential
credential=${credential##https://${id}:}
token=${credential%%@*}
echo "token : ${token}"

echo "Parameters : ${@}"
github_username=${1}
github_reponame=${2}
github_issue_id=${3}
github_body_path=${4}

function print_usage
{
  echo "[GitHub] Update Issue"
  echo "(Usage) ${0} (user name) (repo name) (issue id) (file to update)"
  echo "(Example) ${0} boyinblue blog_automation 1 tmp/list.html"
}

if [ "${github_username}" == "" ]; then
  echo "[Error] username is empty."
  print_usage
  exit 1
elif [ "${github_reponame}" == "" ]; then
  echo "[Error] reponame is empty."
  print_usage
  exit 2
elif [ "${github_issue_id}" == "" ]; then
  echo "[Error] issue id is empty."
  print_usage
  exit 3
elif [ "${github_body_path}" == "" ]; then
  echo "[Error] content to update is empty."
  print_usage
  exit 4
fi

function update_issue
{
  body=$(cat ${github_body_path})
  body=${body//\"/\\\"}

  json="{ \"body\" : \"${body}\" }"

  echo ${json} | \
    curl \
    -u ${id}:${token} \
    -X PATCH \
    -H "Accept: application/vnd.github.v3+json" \
    --data-binary @- \
    https://api.github.com/repos/${github_username}/${github_reponame}/issues/${github_issue_id}
}

update_issue
