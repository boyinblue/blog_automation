#!/bin/bash

KEY_CODE=$(cat token.txt)
URL="https://www.opinet.co.kr/api/avgAllPrice.do?out=json&code=${KEY_CODE}"
DATE=$(date "+%Y-%m-%d")
OUTPUT="tmp/${DATE}/oil_price.json"

mkdir -p tmp/${DATE}

echo "TOKEN : ${KEY_CODE}"

#curl --request GET \
#     --url "https://www.opinet.co.kr/api/avgAllPrice.do?out=json&code=${KEY_CODE}"

wget $URL -O ${OUTPUT}
