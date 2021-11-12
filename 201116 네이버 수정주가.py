import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import Series, DataFrame

# 네이버 금융에서 종목 가격정보와 거래량을 가져오는 함수: get_price

def get_price(company_code):
    # count=3000에서 3000은 과거 3,000 영업일간의 데이터를 의미. 사용자가 조절 가능
    url = "https://fchart.stock.naver.com/sise.nhn?symbol={}&timeframe=day&count=3000&requestType=0".format(
        company_code)
    get_result = requests.get(url)
    bs_obj = BeautifulSoup(get_result.content, "html.parser")

    # information
    inf = bs_obj.select('item')
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df_inf = pd.DataFrame([], columns=columns, index=range(len(inf)))

    for i in range(len(inf)):
        df_inf.iloc[i] = str(inf[i]['data']).split('|')

    df_inf.index = pd.to_datetime(df_inf['Date'])

    return df_inf.drop('Date', axis=1).astype(float)

#test 삼성전자
samsung = get_price('005930')

sample = get_price('077280')

def get_price(company_code, date_std):
    # count=3000에서 3000은 과거 3,000 영업일간의 데이터를 의미. 사용자가 조절 가능
    url = "https://fchart.stock.naver.com/sise.nhn?symbol={}&timeframe=day&count=3000&requestType=0".format(
        company_code)
    get_result = requests.get(url)
    bs_obj = BeautifulSoup(get_result.content, "html.parser")

    # information
    inf = bs_obj.select('item')
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df_inf = pd.DataFrame([], columns=columns, index=range(len(inf)))

    for i in range(len(inf)):
        df_inf.iloc[i] = str(inf[i]['data']).split('|')

    df_inf.index = pd.to_datetime(df_inf['Date'])
    df_inf = df_inf.drop('Date', axis=1).astype(float)
    df_inf = df_inf[date_std:]
    return df_inf

samsung = get_price('005930','2020-11-16')