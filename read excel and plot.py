import pandas as pd
from pandas import Series, DataFrame
from quant_functions import thinning_data_asc, thinning_data_des
from quant_functions import *
import matplotlib.pyplot as plt

FILE = '200726_시총EBITDA, 모멘텀x 선별 소형주20퍼이하 부채비율100, 20개 from 191022_backtest.xlsx'
data = pd.read_excel(FILE,index_col = 0 )
plt.plot(data.index, data['총합계'])
FILE = '200726_시총EBITDA, 모멘텀 선별 소형주20퍼이하 부채비율100, 20개 from 191022_backtest.xlsx'
data = pd.read_excel(FILE,index_col = 0 )
plt.plot(data.index, data['총합계'])
FILE = '200629_EV_EBITDA 순위, 모멘텀순위 부채 100이하 20종목, from 181026__backtest.xlsx'
data = pd.read_excel(FILE,index_col = 0 )
plt.plot(data.index, data['총합계'])