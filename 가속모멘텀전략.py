import pandas as pd
from pandas import Series, DataFrame
from quant_functions import thinning_data_asc, thinning_data_des
from quant_functions import *
 #  data = pd.read_excel('test.xlsx', idex_col = 'A', parse_cols = item)
PER = "발표\nPER"
PBR = "발표\nPBR"
PCR = "과거\nPCR"
PSR = "발표\nPSR"
GPA ="과거\nGP/A\n(%)"
주가 = '주가\n(원)'
부채 = '부채\n비율\n(%)'
모멘텀_1년 = "1년\n등락율\n(%)"
모멘텀_6개월 = "6개월\n등락율\n(%)"
모멘텀_3개월 = "3개월\n등락율\n(%)"
모멘텀_1개월 = "1개월\n등락률\n(%)"
FILE = 'test1.xlsx'
FILENAME = "180815_가속모멘텀"
FILE_SAVE = "{FILENAME}_포트.xlsx".format(FILENAME=FILENAME)
FILE_backtest = "{FILENAME}_backtest.xlsx".format(FILENAME=FILENAME)
data = pd.read_excel(FILE,index_col = 0 )

#스팩 제거
for item in data.index:
    if data["업종\n(소)"][item] == "스팩":
        data=data.drop([item])

#시가총액 하위 20퍼
#data = ltoh_percent(data, '시가총액\n(억)', 20)
#부채비율
#data = data[data[부채]<75]
# PBR 0.2 이하 제외, 시가총액 하위 20%
data = data[data[PBR]>0.2]
#data = data[data[PSR]>0.001]
#data = data[data[PER]>0.001]
#data = data[data[PCR]>0.001]
#모멘텀 >0
data = data[data[모멘텀_1년]>0]
data = data[data[모멘텀_6개월]>data[모멘텀_1년]]
data = data[data[모멘텀_3개월]>data[모멘텀_6개월]]
data = data[data[모멘텀_1개월]>data[모멘텀_3개월]]

PBR_rank = data[PBR].rank(axis=0)
PER_rank = data[PER].rank(axis=0)
PSR_rank = data[PSR].rank(axis=0)
GPA_rank = data[GPA].rank(axis=0, ascending = False)
sum_가치_rank = (PBR_rank+PER_rank+PSR_rank+GPA_rank).rank(axis=0)


sum_rank = (sum_가치_rank).rank(axis =0)
sum_rank = sum_rank.sort_values()

data.insert(len(data.columns),"PBR_rank",PBR_rank)
data.insert(len(data.columns),"PER_rank",PER_rank)
data.insert(len(data.columns),"PSR_rank",PSR_rank)
data.insert(len(data.columns),"GPA_rank",GPA_rank)
data.insert(len(data.columns),"total rank",sum_rank)
'''newdata.insert(1,"PBR_rank",PBR_rank)
newdata.insert(1,"GP/A-rank",GPA_rank)
newdata.insert(1,"total rank",sum_rank)'''
data = data.sort_values(by=['total rank'])
data = data.head(50)
data = data[data[모멘텀_1년]>0]

data.to_excel(FILE_SAVE, "w")
stocklist = data.head(50).index.tolist()
for i in range(0,len(stocklist)):
    stocklist[i]=stocklist[i].replace("A","")

month_data = month_naver_fromto(stocklist,1,32)
data1 = back_test(month_data, 0)
data1.to_excel(FILE_backtest, "w")