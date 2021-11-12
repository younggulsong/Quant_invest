import pandas as pd
from pandas import Series, DataFrame
from quant_functions import thinning_data_asc, thinning_data_des
from quant_functions import ltoh_percent, htol_percent, month_naver, back_test
 #  data = pd.read_excel('test.xlsx', idex_col = 'A', parse_cols = item)
유동자산 = "유동자산\n(억)"
총부채 = "부채\n(억)"
세후이익 = "순이익(지배)\n(억)"
시가총액 = "시가총액\n(억)"
PER = "발표\nPER"
PER_5년 = "5년평균\nPER"
PBR = "발표\nPBR"
PBR_5년 = "5년평균\nPBR"
PCR = "과거\nPCR"
PSR = "발표\nPSR"
GPA ="과거\nGP/A\n(%)"
주가 = '주가\n(원)'
부채 = '단순\n부채비율\n(%)'
모멘텀_1년 = "1년\n등락율\n(%)"
모멘텀_6개월 = "6개월\n등락율\n(%)"
모멘텀_3개월 = "3개월\n등락율\n(%)"
모멘텀_1개월 = "1개월\n등락률\n(%)"
FILE = 'test1.xlsx'
FILE_SAVE = "result_PBR,PER 5년평균이하.xlsx"
FILE_backtest = "180725_PBR,PER 5년평균이하_10개.xlsx"
data = pd.read_excel(FILE,index_col = 0 )

#스팩 제거
for item in data.index:
    if data["업종\n(소)"][item] == "스팩":
        data=data.drop([item])

data = ltoh_percent(data, '시가총액\n(억)', 20)
data = data[data[PBR]>0.2]
data = data[data[PER]>0.001]
# 5년평균 보다 작은것만 골라낸다.
data = data[data[PBR_5년]-data[PBR]>0]
data = data[data[PER_5년]-data[PER]>0]
#PER,PBR 순위
PBR_rank = data[PBR].rank(axis=0)
PER_rank = data[PER].rank(axis=0)

sum_rank = (PBR_rank+PER_rank).rank(axis =0)
sum_rank = sum_rank.sort_values()
data.insert(len(data.columns),"PBR_rank",PBR_rank)
data.insert(len(data.columns),"PER_rank",PER_rank)
data.insert(len(data.columns),"total rank",sum_rank)
data = data.sort_values(by=['total rank'])
data.to_excel(FILE_SAVE, "w")


stocklist = data.head(30).index.tolist()
for i in range(0,len(stocklist)):
    stocklist[i]=stocklist[i].replace("A","")

month_data = month_naver(stocklist, 30)
data1 = back_test(month_data, 0)
data1.to_excel(FILE_backtest, "w")