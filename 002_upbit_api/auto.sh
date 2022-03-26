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

if [ "${1:0:6}" == "-date=" ]; then
  date="${1:6}T23:59:59"
else
  # 임시 디렉토리
  date=$(date -u '+%Y-%m-%dT%H:%m:%d')
fi

yesterday=$(date "--date=$date -d -1day" "+%Y-%m-%d")

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
python3 002_upbit_get_daily_candle.py -date=${yesterday}
python3 003_make_report_per_market.py -date=${yesterday}

# GitHub에 자동으로 업데이트 한다.
pushd ${TARGET_DIR}
git pull
git add ..
git commit -m "[UPBit] auto generated site map & main page"
git push origin main
popd
