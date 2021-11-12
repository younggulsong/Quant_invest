import pandas as pd
from pandas import Series, DataFrame
from quant_functions import thinning_data_asc, thinning_data_des
from quant_functions import ltoh_percent, htol_percent, month_naver, back_test
 #  data = pd.read_excel('test.xlsx', idex_col = 'A', parse_cols = item)
PER = "발표\nPER"
PBR = "발표\nPBR"
PCR = "과거\nPCR"
PSR = "발표\nPSR"
GPA ="과거\nGP/A\n(%)"
주가 = '주가\n(원)'
부채 = '단순\n부채비율\n(%)'
모멘텀_1년 = "1년\n등락율\n(%)"
모멘텀_6개월 = "6개월\n등락율\n(%)"
모멘텀_3개월 = "3개월\n등락율\n(%)"
모멘텀_1개월 = "1개월\n등락률\n(%)"
FILE = 'quantking180309.xlsx'
FILE_SAVE = "181224result_파마_LSV.xlsx"
FILE_backtest = "181224backtest_파마_LSV.xlsx"
data = pd.read_excel(FILE,index_col = 0 )

#스팩 제거
for item in data.index:
    if data["업종\n(소)"][item] == "스팩":
        data=data.drop([item])


# PBR 0.2 이하 제외, 시가총액 하위 20%
data = data[data[PBR]>0.2]
data = data[data[PSR]>0.001]
data = data[data[PER]>0.001]
data = data[data[PCR]>0.001]
#시가총액 하위 500개
data = ltoh_percent(data, '시가총액\n(억)', 50)
#12개월 모멘텀 >0
data = data[data[모멘텀_1년]>0]
#data = data[data[모멘텀_6개월]>0]
#data = data[data[모멘텀_3개월]>0]
#data = data[data[모멘텀_1개월]>0]
#data = data[data["부채\n비율\n(%)"]<100]
#data = data[data[부채]<100]

#newdata = thinning_data_des(newdata, 주가, 150000)
#newdata = thinning_data_des(newdata, 부채, 100)

PBR_rank = data[PBR].rank(axis=0)
PER_rank = data[PER].rank(axis=0)
PCR_rank = data[PCR].rank(axis=0)

sum_rank = (PBR_rank+PER_rank+PCR_rank).rank(axis =0)
sum_rank = sum_rank.sort_values()

data.insert(len(data.columns),"PBR_rank",PBR_rank)
data.insert(len(data.columns),"PER_rank",PER_rank)
data.insert(len(data.columns),"PCR_rank",PCR_rank)
data.insert(len(data.columns),"total rank",sum_rank)
'''newdata.insert(1,"PBR_rank",PBR_rank)
newdata.insert(1,"GP/A-rank",GPA_rank)
newdata.insert(1,"total rank",sum_rank)'''
data = data.sort_values(by=['total rank'])

data.to_excel(FILE_SAVE, "w")


stocklist = data.head(30).index.tolist()
for i in range(0,len(stocklist)):
    stocklist[i]=stocklist[i].replace("A","")

month_data = month_naver(stocklist, 20)
data1 = back_test(month_data, 0)
data1.to_excel(FILE_backtest, "w")