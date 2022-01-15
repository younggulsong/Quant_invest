from pykrx import stock  #https://defineall.tistory.com/746 #https://github.com/sharebook-kr/pykrx
import pykrx
from Investstrategy import *
import pandas as pd
import matplotlib.pyplot as plt
import investpy
import mplfinance as mpf #https://github.com/matplotlib/mplfinance/blob/master/examples/addplot.ipynb

for ticker in stock.get_index_ticker_list(market='KOSDAQ'):
    print(ticker, stock.get_index_ticker_name(ticker))

df = stock.get_index_ohlcv("20200109","20220111","1001")
df.columns = ['open','high','low','close','volume','거래대금']
df['변동성'] = (df['high']-df['low'])/df['close']
df['min변동성'] = df['변동성'].rolling(window=3).min()

colorset = mpf.make_marketcolors(up='tab:red', down='tab:blue', volume='tab:blue',inherit=True)
s = mpf.make_mpf_style(marketcolors=colorset,gridstyle = '--',gridcolor = 'gray')
apdict1 = mpf.make_addplot(df['변동성'],color='gray',width = 1)
apdict2 = mpf.make_addplot(df['min변동성'],width=3, color='r')
apdict = [apdict1,apdict2]
mpf.plot(df, type = 'candle',style=s, addplot=apdict)
