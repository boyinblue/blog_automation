# Query로 수신한 json을 다루기 위한 패키지
import json

# 결과 데이터를 그래프로 그려주기 위함
import matplotlib.pyplot as plt

# 명령행의 가변인자를 처리하기 위함
import sys

# 파일의 존재 여부를 확인하기 위함
import os

# 날짜를 계산하기 위한 패키지
import datetime


TARGET_DIR = 'target_dir'
date = ""
market = ""

# Parsing Command Parameters
for i in range( 1, len(sys.argv) ):
    print("[ARG] " + sys.argv[i])
    if "-date=" in sys.argv[i]:
        date = sys.argv[i][6:]
        print("Date : ", date)
    elif "-market=" in sys.argv[i]:
        market = sys.argv[i][8:]
        print("Market : ", market)

if date == "":
    print("Please set date to analysis")
    exit()

def draw_graph():
    plt.plot(days, trade_price)

#    print(candle_date_time_utc)

    plt.savefig(filename + ".png")

#    plt.show()

def write_table(date, filename, title, description, json_data):
    with open(filename + ".md", 'w') as f:
        f.write("---\n")
        f.write("title: {}\n".format(title))
        f.write("description: {}\n".format(title))
        f.write("---\n")
        f.write("\n")
        f.write("{}\n".format(title))
        f.write("===\n")
        f.write("\n")
        f.write("(단위 : 천원)")
        f.write("|날짜|시가|저가|고가|종가|비고|\n")
        f.write("|--|--|--|--|--|--|\n")
        for candle_json_data in json_data:
            f.write("|{}|{}|{}|{}|{}|    |\n".format(
                candle_json_data['candle_date_time_kst'][:10],
                candle_json_data['opening_price'] / 1000,
                candle_json_data['low_price'] / 1000,
                candle_json_data['high_price'] / 1000,
                candle_json_data['trade_price'] / 1000 ) )

def write_readme(date, json_data):
    readme_filename = "{}/{}/README.md".format(TARGET_DIR, date)
    print("Writing File : {}".format(readme_filename))
    f_readme = open(readme_filename, 'w')
    f_readme.write("---\n")
    f_readme.write("title: 가상화폐 일간 통계 ({})\n".format(date))
    f_readme.write("description: 가상화폐 일간 통계 ({})\n".format(date))
    f_readme.write("---\n")
    f_readme.write("\n")

    f_readme.write("|종목|종목 코드|종가|거래량|전일 대비|변화량|링크|\n")
    f_readme.write("|--|--|--|--|--|--|--|\n")
    for single_data in json_data:
        f_readme.write("|{}|{} ({})|{}|{}|{}|{}|[{}]({})\n".format(
            single_data['korean_name'],
            single_data['market'],
            single_data['english_name'],
            single_data['detail'][0]['trade_price'],
            single_data['detail'][0]['candle_acc_trade_price'],
            single_data['detail'][0]['change_price'],
            single_data['detail'][0]['change_rate'],
            single_data['title'],
            single_data['filename']) )

#if False == os.path.isfile( TARGET_DIR ):
if False == os.path.islink( TARGET_DIR ):
    print("There is no target directory")
    exit()

with open("tmp/market_code.json") as json_file:
    json_data = json.load(json_file)
    for market_json_data in json_data:
        market_name = market_json_data['korean_name']
        market_code = market_json_data['market']
        print( "market : ", market_name )
        title = "가상화폐 일간 통계 ({}, {})".format( market_name, date)
        description = title
#        filename = "/" + date[:10] + "-daily-candle-10days"
        filename = "{}/{}/{}-daily-candle-10days".format( TARGET_DIR, date[:10],market_code )

        market_json_data['title'] = title
        market_json_data['description'] = description
        market_json_data['filename'] = filename

        with open("tmp/{}/daily_candle_{}.json".format(date, market_json_data['market']), 'r') as fp:
            market_json_data['detail'] = json.load(fp)
            write_table(date, filename, title, description, market_json_data['detail'])

    write_readme(date[:10], json_data)