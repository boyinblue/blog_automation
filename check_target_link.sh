#!/bin/bash

declare -A arrData
declare -A arrLinkWarning

BLOG_URL="https://frankler.tistory.com"
if [ "${1}" != "" ]; then
  BLOG_URL="${1}"
fi

function check_link()
{
#  echo "check_link(${filename}, ${line})"

  if [[ "${line}" == *"target="* ]]; then
    arrLinkWarning[${filename}]+="${line}<br>\n"
#    echo "[$filename] ${line}"
  fi
}

function print_link_warning()
{
  echo "${arrLinkWarning[@]}"
}

function get_title()
{
#  echo "get_title(${filename}, ${line})"

  if [[ "${line}" == *"<title>"* ]]; then
    title=${line##<title>}
    title2=${title%%</title>}
    arrKey+="${filename} "
    arrData[${filename}_title]="${title2}"
    arrData[${filename}_url]="${BLOG_URL}/${filename}"
  fi
}

function print_title_info()
{
  echo "<table>"
  echo "  <tr>"
  echo "    <td>No.</td>"
  echo "    <td>URL</td>"
  echo "    <td>Title</td>"
  echo "  </tr>"
  for local_filename in ${arrKey[@]}
  do
    echo "  <tr>"
    echo "    <td>${local_filename}</td>"
    echo "    <td>${arrData[${local_filename}_url]}</td>"
    echo "    <td>${arrData[${local_filename}_title]}</td>"
    echo "  </tr>"
  done
  echo "</table>"
}

function check_next()
{
#  echo "check_next(${line})"

  if [[ "$line" == *"<a href=\"/"* ]]; then
    line2=${line##<a href=\"/}
#    echo "$line"
#    echo "$line2"
    line3=${line2%%\">*}
    number="${line3%%\?*}"
    if [[ "$number" =~ ^[0-9]+$ ]]; then
      download_page "$number"
    elif [ "${number}" != "" ] && [ "${number:0:3}" != "tag" ]; then
      echo "No number : ${number} ${line}"
    fi
  #<a  href='?page=2'>
  elif [[ "$line" == *"<a  href='?page="* ]]; then
    echo "New type : ${line}"
    line2=${line##*<a  href=\'}
    line3=${line2%%\'*}
    echo "$line2"
    echo "$line3"
    if [ "${line3:0:6}" == "?page=" ]; then
      download_page "${line3}"
    fi
  fi
}

function download_page()
{
#  echo "check_page ${1}"
  if [ "${1}" == "" ]; then
    filename="index.html"
    echo "wget -q -O ${filename} ${BLOG_URL}"
    wget -q -O "${filename}" "${BLOG_URL}" >> /dev/null
  elif [ -e ${1} ]; then
    return
  else
    echo "wget -q -O ${1} ${BLOG_URL}/${1}"
    wget -q -O "${1}" "${BLOG_URL}/${1}" >> /dev/null
    filename="${1}"
  fi

  echo "Check file : ${filename}"
  while read line  
  do
    if [[ "$filename" =~ ^[0-9]+$ ]]; then
    check_link ${filename} ${line}
    get_title ${filename} ${line}
    fi
    check_next ${line}
  done < ${filename}
}

rm -rf tmp
mkdir -p tmp
pushd tmp
download_page
popd

print_title_info
print_link_warning
