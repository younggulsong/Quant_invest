import pandas as pd
from pandas import Series, DataFrame
from quant_functions import *
 #  data = pd.read_excel('test.xlsx', idex_col = 'A', parse_cols = item)
Fscore_1 = "F스코어\n지배주주순익>0\n여부"
Fscore_2 = "F스코어\n영업활동현금흐름>0\n여부"
Fscore_3 = "F스코어\n신주발행X\n여부"
GPA ="과거\nGP/A\n(%)"
주가 = '주가\n(원)'
부채 = '단순\n부채비율\n(%)'
FILE = 'test.xlsx'
FILE_SAVE = "result_슈퍼퀄리티_1.xlsx"
FILE_backtest = "backtest_슈퍼퀄리티_1.xlsx"
data = pd.read_excel(FILE,index_col = 0 )
#스팩 제거
for item in data.index:
    if data["업종\n(소)"][item] == "스팩":
        data=data.drop([item])

#시가총액 하위 20%
#data = ltoh_percent(data, '시가총액\n(억)', 20)

# 신 F score 3점만 수집
data = thinning_data_asc(data, Fscore_1, 0.5)
data = thinning_data_asc(data, Fscore_2, 0.5)
data = thinning_data_asc(data, Fscore_3, 0.5)

#data = thinning_data_des(data, 부채, 100)


#newdata = thinning_data_des(newdata, 주가, 150000)
#newdata = thinning_data_des(newdata, 부채, 100)

GPA_rank = data[GPA].rank(axis =0, ascending = False)
data.insert(len(data.columns),"GPA_rank",GPA_rank)

'''newdata.insert(1,"PBR_rank",PBR_rank)
newdata.insert(1,"GP/A-rank",GPA_rank)
newdata.insert(1,"total rank",sum_rank)'''
data = data.sort_values(by=['GPA_rank'])
data.to_excel(FILE_SAVE, "w")

stocklist = data.head(20).index.tolist()
for i in range(0,len(stocklist)):
    stocklist[i]=stocklist[i].replace("A","")

month_data = month_naver(stocklist, 6)
data1 = back_test(month_data, 0.5)
data1.to_excel(FILE_backtest, "w")