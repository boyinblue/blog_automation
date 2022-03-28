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

def change_date_form(str_date):
    date = datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S")
    return datetime.datetime.strftime(date, "%Y년 %m월 %d일 %H시")

def draw_graph():
    plt.plot(days, trade_price)

#    print(candle_date_time_utc)

    plt.savefig(filename + ".png")

#    plt.show()

def write_table(filepath, json_data, detail_json_data):
    with open(filepath + ".md", 'w') as f:
        f.write("---\n")
        f.write("title: {}\n".format(json_data['title']))
        f.write("description: {}\n".format(json_data['description']))
        f.write("---\n")
        f.write("\n")
        f.write("{}\n".format(json_data['title']))
        f.write("===\n")
        f.write("\n")
        f.write("|항목|내용|\n")
        f.write("|--|--|\n")
        f.write("|종목|{}|\n".format(json_data['korean_name']))
        f.write("|마켓|{}|\n".format(json_data['market']))

        scale = json_data['market'].split('-')[0]
        f.write("|단위|{}|\n".format(scale))

        days = json_data['days']
        f.write("|종류|일 단위 캔들 ({}일치)|\n".format(days))

        str_date = detail_json_data[days-1]['candle_date_time_kst']
        str_date_from = change_date_form(str_date)
        str_date = detail_json_data[0]['candle_date_time_kst']
        str_date_to = change_date_form(str_date)
        f.write("|기간|{} - {}|\n".format(str_date_from, str_date_to))

        date = datetime.datetime.today().strftime("%Y년 %m월 %d일 %H시")
        f.write("|생성일|{}|\n".format(date))
        f.write("|출처|[업비트 Open API](https://docs.upbit.com)|\n")
        f.write("\n")
        f.write("\n")

        f.write("|날짜|시가|저가|고가|종가|비고|\n")
        f.write("|--|--|--|--|--|--|\n")
        for candle_json_data in detail_json_data:
            f.write("|{}|{}|{}|{}|{}|    |\n".format(
                candle_json_data['candle_date_time_kst'][:10],
                candle_json_data['opening_price'],
                candle_json_data['low_price'],
                candle_json_data['high_price'],
                candle_json_data['trade_price'] ) )

        f.write("\n")
        f.write("\n")
        f.write("일간 캔들 구간에 대한 설명\n")
        f.write("---\n")
        f.write("\n")
        f.write("\n")
        f.write("업비트의 일간 캔들은 세계 협정시(UTC) 기준입니다. \n")
        f.write("UTC 기준 0시 0분 0초부터 23시 59분 59초까지입니다. \n")
        f.write("한국 시간인 KST 기준으로는 전일 오전 9시부터 다음날 오전 8시 59분까지입니다. \n")
        f.write("\n")
        f.write("\n")

        f.write("예를들면, UTC 기준 3월 25일 데이터는 UTC 시준 3월 25일 0시 0분 0초부터 3월 25일 23시 59분 59초까지입니다. \n")
        f.write("한국 시간으로 표현하면 3월 25일 오전 9시부터 3월 26일 오전 8시 59분까지입니다. \n")
        f.write("이와 같은 이유로 본 페이지는 매일 오전 9시마다 전날의 통계 데이터를 자동으로 작성합니다. \n")
        f.write("\n")
        f.write("\n")

        f.write("주의\n")
        f.write("---\n")
        f.write("\n")
        f.write("\n")
        f.write("본 페이지는 업비트의 Open API를 통하여 자동으로 생성된 페이지입니다. \n")
        f.write("단순한 통계 데이터만 제공하고, 자료를 통해 인사이트를 얻기 위한 참고용으로만 사용하시기 바랍니다. \n")
        f.write("투자를 권유하는 것은 아니며, 투자에 대한 모든 책임은 투자자 본인에게 있습니다. \n")

def write_readme(date, json_data):
    readme_filename = "{}/{}/README.md".format(TARGET_DIR, date)
    title = "가상화폐 일간 통계 ({})".format(date)
    description = title

    print("Writing File : {}".format(readme_filename))
    f_readme = open(readme_filename, 'w')

    f_readme.write("---\n")
    f_readme.write("title: {}\n".format(title))
    f_readme.write("description: {}\n".format(description))
    f_readme.write("---\n")
    f_readme.write("\n")

    f_readme.write("{}\n".format(title))
    f_readme.write("===\n")
    f_readme.write("\n");
    f_readme.write("\n");

    f_readme.write("본 페이지는 업비트에 거래되고 있는 암호화폐들의 일간 캔들 정보를 제공합니다. \n")
    f_readme.write("종목 정보들은 가격 변동율을 기준으로 내림차순 정렬되어 있습니다. \n")
    f_readme.write("세부 링크를 클릭하시면 좀 더 자세한 내용과 그래프를 확인하실 수 있습니다. \n")
    f_readme.write("\n");
    f_readme.write("\n");

    for single_data in json_data:
        print(single_data)
        f_readme.write("[{}]({})\n".format(single_data['title'], single_data['filename']) )
        f_readme.write("\n");
        f_readme.write("|항목|내용|\n")
        f_readme.write("|--|--|\n")
        f_readme.write("|마켓|{}|\n".format(single_data['market']))
        f_readme.write("|종목|{}({})|\n".format(single_data['korean_name'],
            single_data['english_name']))
        f_readme.write("|종가|{}|\n".format(single_data['trade_price']))
        f_readme.write("|누적 거래량|{}|\n".format(single_data['candle_acc_trade_price']))
        f_readme.write("|가격 변화|{}|\n".format(single_data['change_price']))
        f_readme.write("|가격 변동율|{}|\n".format(single_data['change_rate']))
        f_readme.write("\n");
        f_readme.write("\n");

#if False == os.path.isfile( TARGET_DIR ):
if False == os.path.islink( TARGET_DIR ):
    print("There is no target directory")
    exit()

sorted_json_data = []

with open("tmp/market_code.json", 'r') as json_file:
    json_data = json.load(json_file)
    for market_json_data in json_data:
        market_name = market_json_data['korean_name']
        market_code = market_json_data['market']
        print( "market : {} ({})".format(market_code, market_name) )
        title = "가상화폐 일간 통계 ({}, {}, {})".format(
                        market_name, 
                        date,
                        market_code)
        description = title
#       filename = "/" + date[:10] + "-daily-candle-10days"
        filename = "{}-daily-candle-10days.html".format(market_code)
        filepath = "{}/{}/{}-daily-candle-10days".format(
                        TARGET_DIR,
                        date,
                        market_code)

        market_json_data['title'] = title
        market_json_data['description'] = description
        market_json_data['filename'] = filename

        with open("tmp/{}/daily_candle_{}.json".format(date, market_json_data['market']), 'r') as fp:
            detail_json_data = json.load(fp)
            market_json_data['days'] = len(detail_json_data)
            for key in detail_json_data[0].keys():
                market_json_data[key] = detail_json_data[0][key]
            write_table(filepath, market_json_data, detail_json_data)
#            print(market_json_data)
        sorted_json_data.append( market_json_data )

    write_readme(date[:10], sorted_json_data)
