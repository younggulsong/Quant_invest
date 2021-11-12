import pandas as pd
from pandas import Series, DataFrame
from quant_functions import *
from quant_functions import ltoh_percent
 #  data = pd.read_excel('test.xlsx', idex_col = 'A', parse_cols = item)
PBR = "발표\nPBR"
GPA ="과거\nGP/A\n(%)"
주가 = '주가\n(원)'
부채 = '단순\n부채비율\n(%)'
FILE = 'quantking180309.xlsx'
FILE_SAVE = "181224_저PBR_고GPA 포트.xlsx"
FILE_backtest = "181224_저PBR_고GPA_backtest_from180309.xlsx"
data = pd.read_excel(FILE,index_col = 0 )
#스팩 제거
for item in data.index:
    if data["업종\n(소)"][item] == "스팩":
        data=data.drop([item])


data = ltoh_percent(data, '시가총액\n(억)', 20)
# 주가가 너무 높거나 부채비율이 많으면 포트폴리오에서 제외, PBR <0.2도 제외
data = data[data[PBR]>=0.2]
##### PBR, GP/A별로 랭킹

PBR_rank = data[PBR].rank(axis=0)
GPA_rank = data[GPA].rank(axis =0, ascending = False)
sum_rank = (PBR_rank+GPA_rank).rank(axis =0)
sum_rank = sum_rank.sort_values()
data.insert(len(data.columns),"PBR_rank",PBR_rank)
data.insert(len(data.columns),"GP/A-rank",GPA_rank)
data.insert(len(data.columns),"total rank",sum_rank)
'''newdata.insert(1,"PBR_rank",PBR_rank)
newdata.insert(1,"GP/A-rank",GPA_rank)
newdata.insert(1,"total rank",sum_rank)'''
data = data.sort_values(by=['total rank'])


data.to_excel(FILE_SAVE, "w")

stocklist = data.head(30).index.tolist()
for i in range(0,len(stocklist)):
    stocklist[i]=stocklist[i].replace("A","")

month_data = month_naver_fromto(stocklist,1,20)
data1 = back_test(month_data, 0)
data1.to_excel(FILE_backtest, "w")