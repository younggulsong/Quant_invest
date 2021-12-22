#이익모멘텀 이용
import pandas as pd
from pandas import Series, DataFrame
from quant_functions import thinning_data_asc, thinning_data_des
from quant_functions import *
from DBUpdater import *
import matplotlib.pyplot as plt
import datetime
#DataBase update
'''
db = DBUpdater()
db.update_comp_info()
db.update_daily_price(2)
'''

stock = '에디슨EV'
price_list = MarketDB()

code = price_list.companies[stock]

price_list = MarketDB()
today = datetime.datetime.now().strftime('%Y-%m-%d')
start_day = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
stk_price = price_list.get_daily_price(code,start_date=start_day,end_date=today)


stk_price['MA10'] = stk_price['close'].rolling(window=12).mean()
stk_price['MA20'] = stk_price['close'].rolling(window=26).mean()
stk_price['MA60'] = stk_price['close'].rolling(window=60).mean()
stk_price['MACD'] = stk_price['close'].rolling(window=12).mean()-stk_price['close'].rolling(window=26).mean()
stk_price['MACD_signal'] = stk_price['MACD'].rolling(window=9).mean()
stk_price['MACD_osc'] = stk_price['MACD']-stk_price['MACD_signal']
stk_price['pc_upper'] = stk_price['high'].rolling(window=5).max().shift(1)
stk_price['pc_lower'] = stk_price['low'].rolling(window=5).min().shift(1)


plt.figure(figsize=(18,14))
p1 = plt.subplot(2,1,1)
plt.title('first screen_price moving')
plt.rc('font', size=20)
plt.plot(stk_price.index, stk_price['close'],marker='o',markersize=5, label='return avg', linewidth=3, color='gray')
plt.plot(stk_price.index, stk_price['MA10'], color = 'red',label='MA12')
plt.plot(stk_price.index, stk_price['MA20'], color = 'orange',label='MA26')
plt.plot(stk_price.index, stk_price['MA60'], color = 'blue',label='MA60')
plt.plot(stk_price.index, stk_price['pc_upper'], color = 'green',label='pc_upper')
plt.plot(stk_price.index, stk_price['pc_lower'], color = 'green',label='pc_lower')
plt.grid(True)
#plt.legend()
plt.xlim([stk_price.index[0],stk_price.index[-1]+datetime.timedelta(days=20)])
p2 = plt.subplot(2,1,2)
plt.grid(True)
plt.bar(stk_price.index,stk_price['MACD_osc'], color='m',label='MACD-HIST')
plt.plot(stk_price.index,stk_price['MACD'], color='black',label='MACD')
plt.plot(stk_price.index,stk_price['MACD_signal'],'g--',label='MACD-Signal')
plt.xlim([stk_price.index[0],stk_price.index[-1]+datetime.timedelta(days=20)])