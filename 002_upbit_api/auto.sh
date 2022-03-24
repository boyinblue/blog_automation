#!/bin/bash
set -e

# 필요한 파일들
TMP_DIR=tmp
MARKET_CODE_FILE="tmp/market_code.json"
TARGET_DIR='target_dir'

# 환경 변수
TARGET_DIR_DEFAULT='../../boyinblue.github.io/009_upbit'

# GitHub로부터 최신 코드를 수신함
git pull

# 임시 디렉토리
date_utc=$(date -u '+%Y-%m-%d')
date_today=$(date '+%Y-%m-%d')
if [ "${date_utc:10}" == "${date_today:10}" ]; then
  # 오전 9시가 넘으면 UTC 날짜와 동일하므로, 어제 날짜로 디렉토리 생성
  yesterday=$(date -d "yesterday" '+%Y-%m-%d')
else
  # 오전 9시 이전이면 UTC 날짜가 어제 날짜이므로 디렉토리 생성
  yesterday=$date_utc
fi
#echo "mkdir -p $TMP_DIR/${yesterday}"
mkdir -p $TMP_DIR/${yesterday}
mkdir -p ${TARGET_DIR}/${yesterday}

# 자동화의 결과가 저장될 디렉토리 (synbolic link)
if [ ! -d $TARGET_DIR ]; then
  echo "There is no symbolic link"
  if [ -d $TARGET_DIR_DEFAULT ]; then
    echo "Make symbolic link by default"
    ln -s $TARGET_DIR_DEFAULT $TARGET_DIR
  else
    echo "Cannot make symbolic link automatically"
    echo "Because there is no path : $TARGET_DIR_DEFAULT"
  fi
fi

# market.json 파일이 없으면 새로 받아온다.
if [ ! -e $MARKET_CODE_FILE ]; then
  python3 000_upbit_get_market_code.py
fi

# 일간 캔들을 가져온다.
python3 002_upbit_get_daily_candle.py
python3 003_make_report_per_market.py -date=${yesterday}

# GitHub에 자동으로 업데이트 한다.
pushd ${TARGET_DIR}
git add ..
git commit -m "[UPBit] auto generated site map & main page"
git push origin main
popd
