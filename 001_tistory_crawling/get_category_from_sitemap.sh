#!/bin/bash

### 인자에 대한 설명 ###
function print_usage
{
  echo "(Usage) ${0} (Tistory URL)"
  echo "(Example) ${0} https://frankler.tistory.com"
}

### 페이지의 타이틀 가져오기 ###
function get_title
{
  url=${1}
  local_file="tmp/${url##*/}"
  wget ${url} -q -O ${local_file}

  while read line;
  do
    if [[ "${line}" == *"<title>"* ]]; then
      title=${line##*<title>}
      title=${title%</title>*}
    fi
  done < ${local_file}
}

### 전역변수
OUTPUT_FILE="tmp/category.md"

### 임시 디렉토리 생성 및 결과 파일 초기화 ###
mkdir -p tmp
rm -f "${OUTPUT_FILE}"

### 인자 개수가 하나도 없을 경우 종료 ###
if [ "${1}" == "" ]; then
  print_usage
  exit -1
fi

### 사이트맵 다운로드 ###
echo "URL : ${1}"
sitemap="sitemap.xml"
sitemap_url="${1}/${sitemap}"
sitemap_local="tmp/${sitemap}"
echo "Download Sitemap : ${sitemap_url}"
wget $sitemap_url -q -O $sitemap_local

### 다운로드 실패시 예외 처리 ###
if [ ! -e ${sitemap_local} ]; then
  echo "No sitemap"
  exit -2
fi

### 사이트맵 파싱 ###
while read line;
do
  if [[ "$line" == *"loc"* ]]; then
    link=${line##*<loc>}
    link=${link%</loc>*}
    if [[ "$line" == *"/category/"* ]]; then
      echo ""
      echo $link
      title=""
      get_title ${link}
      echo "- [${title}](${link})" | tee -a ${OUTPUT_FILE}
    fi
  fi
done < ${sitemap_local}
