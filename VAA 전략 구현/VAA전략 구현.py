# 다음 사이트 기반으로 작성 https://jacobjinwonlee.github.io/pythonproject/2021/06/06/pythonproject-backtest-vaa/

import pandas as pd
import pandas_datareader as pdr
from datetime import datetime, timedelta
import backtrader as bt
import numpy as np
from matplotlib import pyplot as plt
import pyfolio as pf
import quantstats
import math
import seaborn
import yfinance as yf


'''
yf.pdr_override()

start = datetime(2021,6,1)
end = datetime(2021,6,29)

tickers = ['SPY','EFA','EEM','AGG','LQD','SHY','IEF']

def get_price_data(tickers):
    df_asset = pd.DataFrame(columns=tickers)

    for ticker in tickers:
        df_asset[ticker] = pdr.get_data_yahoo(ticker, start, end)['Adj Close']

    return df_asset

df_asset['SPY'] = pdr.get_data_yahoo('SPY', "2021-06-01", "2021-06-10")

pdr.get_data_yahoo('')

df = pdr.get_data_yahoo('SPY')
''' #yahoo finance가 안되서.. 일단봉인


##
FILE = 'LQD.csv'
data_LQD = pd.read_csv("VAA 전략 구현/{FILE}".format(FILE=FILE),index_col = 0 )["Adj Close"]
FILE = 'SPY.csv'
data_SPY = pd.read_csv("VAA 전략 구현/{FILE}".format(FILE=FILE),index_col = 0 )["Adj Close"]

data_merge = pd.merge(data_LQD,data_SPY, left_index=True, right_index=True, how='outer')
import os

path = 'VAA 전략 구현/'
file_list = os.listdir(path)
csv_list = [file for file in file_list if file.endswith(".csv")]

VAA_data = pd.DataFrame()
#['AGG.csv', 'IEF.csv', 'LQD.csv', 'SHY.csv', 'SPY.csv', 'VEA.csv', 'VWO.csv']
for file in csv_list:
    data = pd.read_csv("VAA 전략 구현/{FILE}".format(FILE=file),index_col = 0 )["Adj Close"]
    VAA_data = pd.merge(VAA_data, data, left_index=True, right_index=True, how='outer')
    print(VAA_data.head(5))
VAA_data = VAA_data.dropna(axis=0)
VAA_data.columns = ['AGG', 'IEF', 'LQD', 'SHY', 'SPY', 'VEA', 'VWO']

for column in VAA_data.columns:
    수익_12개월 = VAA_data[column]/VAA_data[column].shift(240) - 1
    수익_6개월 = VAA_data[column]/VAA_data[column].shift(120) - 1
    수익_3개월 = VAA_data[column]/VAA_data[column].shift(60) - 1
    수익_1개월 = VAA_data[column]/VAA_data[column].shift(20) - 1
    momentum = 12*수익_1개월 + 4*수익_3개월 + 2*수익_6개월 + 수익_12개월
    VAA_data.insert(len(VAA_data.columns), "{name}_mom".format(name=column), momentum)
VAA_data = VAA_data.dropna(axis=0)
#한달 data만 빼고 다 지우기 back test를 위해

indexlist = [index for i,index in enumerate(VAA_data[::-1].index) if np.mod(i,20) >0.5]
VAA_data_month = VAA_data.drop(indexlist)
#여기까지 성공 이제 모멘텀 기준을 따라서 자산점검을 해야
VAA_data_month.to_excel("VAA 전략 구현/VAA전략.xlsx","w")