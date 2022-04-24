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

stock = 'SK하이닉스'
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




df = stock_back_week(stk_price_week, k=0.4)
plt.plot(df.index, df['누적수익률'],label=f'Basic VB')
plt.plot(df.index, df['기본수익률'],label=f'basic earn')
plt.legend()

df = stock_back_week_long_ts(stk_price_week,k=0.4)
plt.plot(df.index, df['누적수익률'],label=f'VB_long')
plt.legend()
#뭔가 이상한 price channel을 제대로 따라가는게 아닌거 같아
df = price_channel(stk_price, pc_upper_day=20, pc_lower_day=10)
plt.plot(df.index, df['기본수익률'],label='기본수익')
plt.plot(df.index, df['누적수익률'],label='누적수익')
plt.legend()


def price_channel(df, pc_upper_day, pc_lower_day):  # price channel과 관련된 전략
    price=df
    수수료율 = 0.0015
    status = 0
    price['일일수익률'] = 1.

    price['일일수익률'] = 1.
    price['누적수익률'] = 1.
    price['진입당수익률'] = 1.
    price['max대비손실'] = 0.
    price['기본수익률'] = price['close'] / price['close'][0]
    price['pc_upper'] = price.rolling(window=pc_upper_day)['high'].max().shift(1)
    price['pc_lower'] = price.rolling(window=pc_lower_day)['low'].min().shift(1)

    for i, date in enumerate(price.index):

        if i < 7:  # 초기 7일은 전주가 없으므로 거래 제외
            continue
        day_1 = price.index[i-1]
        price.loc[day_1, 'max대비손실'] = -100 * (1 - price.loc[day_1, '누적수익률'] / price.loc[:day_1, '누적수익률'].max())
        if status == 0:  # 안산 상태이면 high 값이 upper channel 보다 높을 때 upper channel로 구매
            if price.loc[date, 'high'] > price.loc[date, 'pc_upper']:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'pc_upper']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                진입가격 = price.loc[date, 'pc_upper']
                status = 1
                continue
            else:
                price.loc[date, '일일수익률'] = 1.
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

        if status == 1:  # 산 상태이면 low 값이 below channel 보다 높을 때 lower channel로 판매
            sellprice = price.loc[date, 'pc_lower'] #price channel 하단에서 판다
            if price.loc[date, 'low'] < sellprice:
                price.loc[date, '일일수익률'] = sellprice / price.loc[date, 'open'] * ((1 - 수수료율) ** 2)
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                price.loc[date, '진입당수익률'] = sellprice / 진입가격 * ((1 - 수수료율) ** 2)
                status = 0  # 손절하여 매도 상태
                continue
            else:
                price.loc[date, '일일수익률'] = price.loc[date, 'close'] / price.loc[date, 'open']
                price.loc[date, '누적수익률'] = price.loc[date, '일일수익률'] * price.loc[day_1, '누적수익률']
                continue

    return price
