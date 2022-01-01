#이익모멘텀 이용
import pandas as pd
from pandas import Series, DataFrame
from quant_functions import thinning_data_asc, thinning_data_des
from quant_functions import *
from DBUpdater import *
import matplotlib.pyplot as plt
import datetime
from Investstrategy import *
from pykrx import stock  #https://defineall.tistory.com/746
import pykrx

stock = '카카오'
price_list = MarketDB()
#price = pykrx.stock.get_market_ohlcv_by_date()
#df = pykrx.stock.get_market_ohlcv_by_date("20150720", "20150810", "005930","m")
#df.columns = ['open','high','low','close','volume']

code = price_list.companies[stock]
today = datetime.datetime.now().strftime('%Y-%m-%d')
start_day = (datetime.datetime.now() - datetime.timedelta(days=1000)).strftime('%Y-%m-%d')
stk_price = price_list.get_daily_price(code,start_date=start_day,end_date=today)

stk_price_week=stk_price
#주봉만들기
for i, date in enumerate(stk_price.index):
    if i%5 ==0 :
        high = stk_price.iloc[i:i+5]['high'].max()
        low = stk_price.iloc[i:i+5]['low'].min()
        open = stk_price.iloc[i]['open']
        close = stk_price.iloc[i:i+5]['close'][-1]
        stk_price_week.loc[date,'high'] = high
        stk_price_week.loc[date,'low'] = low
        stk_price_week.loc[date,'open'] = open
        stk_price_week.loc[date,'close'] = close
        continue
    stk_price_week = stk_price_week.drop(index=date)




df = stock_back_week(stk_price_week, k=0.5)
plt.plot(df.index, df['누적수익률'],label=f'Basic VB')
plt.plot(df.index, df['기본수익률'],label=f'basic earn')
plt.legend()