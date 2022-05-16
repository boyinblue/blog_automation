#!/bin/bash

EPASS_URL="https://www.e-pass.co.kr"

function download_js()
{
  while read line;
  do
    if [[ ${line} != *"script"* ]]; then
      continue
    elif [[ ${line} != *"src="* ]]; then
      continue
    fi

    echo "$line"
  done < ${1}
}

download_js ${1}
