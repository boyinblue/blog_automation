# Upbit API를 사용하기 위한 패키지
import requests

# Query로 수신한 json을 다루기 위한 패키지
import json

# 결과 데이터를 그래프로 그려주기 위함
import matplotlib.pyplot as plt

# 파일의 존재 여부를 확인하기 위함
import os


TARGET_DIR = 'target_dir'

days = list(range(10))
opening_price=[]
high_price=[]
low_price=[]
trade_price=[]
candle_date_time_utc=[]

def select_opening_price(abc):
    return abc['opening_price']
    
def select_high_price(abc):
    return abc['high_price']

def select_low_price(abc):
    return abc['low_price']

def select_trade_price(abc):
    return abc['trade_price']

def select_date_time_utc(abc):
    return abc['candle_date_time_utc']

def load_data_from_upbit():
    global opening_price
    global high_price
    global low_price
    global trade_price
    global candle_date_time_utc
    global date
    global title
    global description
    global filename

    url = "https://api.upbit.com/v1/candles/days?market=KRW-BTC&count=10"
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    #print(response.text)

    st_python = json.loads(response.text)
    #print(st_python)

    opening_price=list(map(select_opening_price, st_python))
    high_price=list(map(select_high_price, st_python))
    low_price=list(map(select_low_price, st_python))
    trade_price=list(map(select_trade_price, st_python))
    candle_date_time_utc=list(map(select_date_time_utc, st_python))

    date = candle_date_time_utc[0]
    title = "업비트 일간 캔들 조회(" + date + ")"
    description = title
#    filename = "/" + date[:10] + "-daily-candle-10days"
    filename = "{}/{}-daily-candle-10days".format( TARGET_DIR, date[:10] )

def draw_graph():
    plt.plot(days, opening_price)
    plt.plot(days, high_price)
    plt.plot(days, low_price)
    plt.plot(days, trade_price)

    print(candle_date_time_utc)

    plt.savefig(filename + ".png")

#    plt.show()

def write_table():

    with open(filename + ".md", 'w') as f:
        f.write("---\n")
        f.write("title: {}\n".format(title))
        f.write("description: {}\n".format(title))
        f.write("---\n")
        f.write("\n")
        f.write("{}\n".format(title))
        f.write("===\n")
        f.write("\n")
        f.write("|날짜|시가|저가|고가|종가|비고|\n")
        f.write("|--|--|--|--|--|--|\n")
        for i in days:
            f.write("|{}|{}|{}|{}|{}|    |\n".format(
                candle_date_time_utc[i],
                opening_price[i],
                low_price[i],
                high_price[i],
                trade_price[i]))

if False == os.path.isfile( TARGET_DIR ):
    print("There is no target directory")

load_data_from_upbit()
draw_graph()
write_table()
