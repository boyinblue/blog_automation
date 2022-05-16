#!/bin/bash

EPASS_URL="https://www.e-pass.co.kr"

function get_list()
{
  curl -H "Content-Type: application/x-www-form-urlencoded" \
          "$EPASS_URL" | iconv -f euc-kr -t utf-8 | tee tmp/list.html

  cat tmp/list.html | grep new_info | tee tmp/prime_list.txt

  while read line;
  do
    if [[ ${line} == *"onMouseOver"* ]]; then
      continue
    fi
    line=${line##*<a href=\"}
    line=${line%%&amp*}
    echo "$line"

    no=${line##*?InNo=}
    echo "$no"

    get_sub_list $no
  done < tmp/prime_list.txt
}

function get_sub_list()
{
  echo get_sub_list $1

  if [ -e tmp/${1}.raw ]; then
    echo "skip!"
  fi

  curl -s -H "Content-Type: application/x-www-form-urlencoded" \
          "${EPASS_URL}/event/new_info.asp?InNo=${1}" \
          | iconv -f euc-kr -t utf-8 > tmp/${1}.raw

  prime=$(cat tmp/${1}.raw | grep name=\"description\")

  period=${prime##*2.응모기간 : }
  period=${period%%3.경품*}
  
  goods=${prime##*3.경품: }
  goods=${goods%%\" />*}

  echo ${prime}
  echo "응모기간 : ${period}" | tee ${1}.txt
  echo "경품 : ${goods}" | tee -a ${1}.txt

  curl -s -d "InNo=${1}&EnType=B" \
          -H "Content-Type: application/x-www-form-urlencoded" \
          -X POST ${EPASS_URL}/eventinfo/get_event_url.asp \
       | iconv -f euc-kr -t utf-8 > tmp/${1}.html

  link=$(cat tmp/${1}.html | grep location.href)
  link=${link##location.href=}
  link=${link%%;*}
  echo "링크 : $link" | tee -a ${1}.txt
}

mkdir -p tmp

get_list
