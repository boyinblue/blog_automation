# Upbit API를 사용하기 위한 패키지
import requests

# Query로 수신한 json을 다루기 위한 패키지
import json

# json decode error exception
from json.decoder import JSONDecodeError

# 날짜를 계산하기 위한 패키지
import datetime

# 너무 빈번한 API 호출을 피하기 위해 sleep 사용
import time

# 명령행 인자 파싱을 위한 패키지
import sys

def print_usage():
    print("(Usage) ${0} -date=(date)")
    print("(Example) ${0} -date=2022-03-26")

date = ""

# Parsing Command Parameters
for i in range( 1, len(sys.argv) ):
    print("[ARG] " + sys.argv[i])
    if "-date=" in sys.argv[i]:
        date = sys.argv[i][6:]
        print("Date : ", date)

if date == "":
    print("Please set date")
    print_usage()
    exit(1)

def load_data_from_upbit(date, market_code):

    to_date = date + 'T23:59:59Z';

    url_format = "https://api.upbit.com/v1/candles/days?market={}&count=10&to={}"
    url = url_format.format( market_code, to_date )
    print("Query : ", url)

    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
#    print(response.text)

    st_python = json.loads(response.text)
    #print(st_python)

    with open( "tmp/{}/daily_candle_{}.json".format(to_date[:10], market_code), 'w' ) as fp:
        json.dump(st_python, fp)

    return True

# 마켓 목록을 market_code.json 파일에서 가져옴
with open("tmp/market_code.json") as json_file:
    json_data = json.load(json_file)
    for market_json_data in json_data:
        print(market_json_data)
        for trycnt in range(10):
            try:
                result = load_data_from_upbit(date, market_json_data['market'])
                if result:
                    break
            except JSONDecodeError as e:
                print("JSODecodeError retry", trycnt)
                time.sleep(1)
                pass
            except Exception as e:
                raise e
