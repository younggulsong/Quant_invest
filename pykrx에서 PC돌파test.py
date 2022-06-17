from pykrx import stock  #https://defineall.tistory.com/746
import pykrx
from Investstrategy import *
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf #https://github.com/matplotlib/mplfinance/blob/master/examples/addplot.ipynb


tickers = pykrx.stock.get_market_ticker_list("20220104",market="KOSDAQ")
#ETF 가격
df = stock.get_market_ohlcv_by_date("20181021", "20220104", "122630")
df.columns = ['open','high','low','close','volume']
df = stock.get_market_ohlcv_by_date("20140104", "20220128", "233740") #233740:kosdaq 레버리지
df.columns = ['open','high','low','close','volume']

data = pd.DataFrame(columns = ['upper','lower','누적수익률'])
for upper in range(4,84,4):
    for lower in range(4,84,4):
        result = price_channel(df, pc_upper_day=upper, pc_lower_day=lower,sell_ratio=1)
        new_data = {'upper':upper,'lower':lower,'누적수익률':result['누적수익률'][-1]}
        data = data.append(new_data,ignore_index=True)
        print(new_data)
data.to_excel('220129 14년_22년코스닥레버리지233740PC 수익률쏵.xlsx')

upper = 10
lower = 10
result = price_channel(df, pc_upper_day=upper, pc_lower_day=lower, sell_ratio=1)

plt.figure(figsize=(18,14))
p1 = plt.subplot(2,1,1)
plt.title('코스닥 레버리지 PC')
plt.rc('font', size=20)
plt.plot(stk_price.index, stk_price['close'],marker='o',markersize=5, label='return avg', linewidth=3, color='gray')
plt.plot(stk_price.index, stk_price['pc_upper'], color = 'green',label='pc_upper')
plt.plot(stk_price.index, stk_price['pc_lower'], color = 'green',label='pc_lower')

colorset = mpf.make_marketcolors(up='tab:red', down='tab:blue', volume='tab:blue',inherit=True)
s = mpf.make_mpf_style(marketcolors=colorset,gridstyle = '--',gridcolor = 'gray')
apdict1 = mpf.make_addplot(result['pc_upper'],color='green',width = 1)
apdict2 = mpf.make_addplot(result['pc_lower'],color='green',width = 1)
apdict = [apdict1,apdict2]
mpf.plot(result, type = 'candle',style=s, addplot=apdict)
