#!/bin/bash

BLOG_URL="https://frankler.tistory.com"

function check_page()
{
  echo "check_page ${1}"
  if [ "${1}" == "" ]; then
    filename="index.html"
    echo "wget ${BLOG_URL}"
    wget -O "${filename}" "${BLOG_URL}" >> /dev/null
  elif [ -e ${1} ]; then
    return
  else
    echo "wget ${BLOG_URL}/${1}"
    wget -O "${1}" "${BLOG_URL}/${1}" >> /dev/null
    filename="${1}"
  fi

  echo "Check file : ${filename}"
  while read line  
  do
    if [[ "$line" == *"target="* ]]; then
      echo "[$filename] $line"
    fi
    if [[ "$line" == *"<a href=\"/"* ]]; then
      line2=${line##<a href=\"/}
#      echo "$line"
#      echo "$line2"
      line3=${line2%%\">*}
      number="${line3%%\?*}"
      if [[ "$number" =~ ^[0-9]+$ ]]; then
        echo "$number"
        check_page "$number"
      fi
    fi
  done < ${filename}
}

rm -rf tmp
mkdir -p tmp
pushd tmp
check_page
popd
