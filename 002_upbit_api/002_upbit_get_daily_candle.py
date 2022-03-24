# Upbit API를 사용하기 위한 패키지
import requests

# Query로 수신한 json을 다루기 위한 패키지
import json

# 날짜를 계산하기 위한 패키지
import datetime

today_date = datetime.datetime.today()
yesterday_date = today_date - datetime.timedelta(1)

print("오늘 날짜 : " + today_date.strftime('%Y-%m-%dT%H:%m:%dZ'))
print("어제 날짜 : " + yesterday_date.strftime('%Y-%m-%dT%H:%m:%dZ'))

def load_data_from_upbit(date, market_code):

    to_date = date.strftime('%Y-%m-%dT%H:%m:%dZ');

    url_format = "https://api.upbit.com/v1/candles/days?market={}&count=10&to={}"
    url = url_format.format( market_code, to_date )
    print("Query : ", url)

    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    #print(response.text)

    st_python = json.loads(response.text)
    #print(st_python)

    with open( "tmp/{}/daily_candle_{}.json".format(to_date[:10], market_code), 'w' ) as fp:
        json.dump(st_python, fp)

# 마켓 목록을 market_code.json 파일에서 가져옴
with open("tmp/market_code.json") as json_file:
    json_data = json.load(json_file)
    for market_json_data in json_data:
        print(market_json_data)
        load_data_from_upbit(yesterday_date, market_json_data['market'])
#        load_data_from_upbit(today_date, market_json_data['market'])
