#!/bin/bash

EPASS_URL="https://www.e-pass.co.kr"
event_title=""

function get_list()
{
  # 웹페이지에서 이벤트 목록을 가져온다
  wget $EPASS_URL -q -O tmp/list.html
  cat tmp/list.html | grep new_info | iconv -f euc-kr -t utf-8 > tmp/prime_list.dat

  while read line;
  do
    if [[ ${line} == *"onMouseOver"* ]]; then
      continue
    fi

    echo ""

    line=${line##*<a href=\"}
    line=${line%%&amp*}
#    echo "$line"

    no=${line##*?InNo=}
    echo "[$no]"

    get_sub_list $no
  done < tmp/prime_list.dat
}

function get_event_title()
{
#  echo "Get Title : ${2}"
  wget ${2} -T 5 -t 1 -q -O ${1}/title.html
  if [ $? != 0 ]; then
    echo "이벤트 페이지 연결 불가!"
    echo "  - ID : ${1}"
    echo "  - URL : ${2}"
    return 255
  fi

  while read line;
  do
    if [[ ${line} == *"<title>"* ]]; then
      event_title=${line##*<title>}
      event_title=${event_title%%</title>*}
    fi
  done < ${1}/title.html
}

function get_sub_list()
{
  # 개별 이벤트 정보를 가져온다.
  DIR="tmp/${1}"
  mkdir -p ${DIR}

  if [ -e "${DIR}/index.html" ]; then
    echo "이미 처리되었습니다."
    return
  fi

  curl -s -H "Content-Type: application/x-www-form-urlencoded" \
          "${EPASS_URL}/event/new_info.asp?InNo=${1}" \
          | iconv -f euc-kr -t utf-8 > "${DIR}/index.html"

  prime=$(cat ${DIR}/index.html | grep name=\"description\")

  # 이벤트 제목을 가져온다.
  title=${prime#*1.}
  title=${title%% 2.*}

  # 응모기간 정보를 가져온다.
  period=${prime##*2.응모기간 : ~}
  period=${period%%3.경품*}
  
  # 경품 정보를 가져온다. 
  goods=${prime##*3.경품: }
  goods=${goods%%\" />*}

  # 이벤트 응모 URL을 가져온다.
  curl -s -d "InNo=${1}&EnType=B" \
          -H "Content-Type: application/x-www-form-urlencoded" \
          -X POST ${EPASS_URL}/eventinfo/get_event_url.asp \
       | iconv -f euc-kr -t utf-8 > "${DIR}/link.html"

  link=$(cat "${DIR}/link.html" | grep location.href)
  link=${link##location.href=}
  link=${link%%;*}
  link=$(echo $link | xargs)

  # 이벤트 제목을 가져온다.
  event_title=""
  get_event_title ${DIR} ${link}
  if [ "$?" == 255 ]; then
    echo "URL 연결 불가"
  fi

  echo ${prime}
  echo "제목|${title}" | tee "${DIR}/data.txt"
  echo "제목2|${event_title}" | tee "${DIR}/data.txt"
  echo "응모기간|${period}" | tee "${DIR}/data.txt"
  echo "경품|${goods}" | tee -a "${DIR}/data.txt"
  echo "링크|$link" | tee -a "${DIR}/data.txt"
}

mkdir -p tmp

get_list
