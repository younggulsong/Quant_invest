import pandas as pd
from pandas import Series, DataFrame
from quant_functions import thinning_data_asc, thinning_data_des
from quant_functions import *
 #  data = pd.read_excel('test.xlsx', idex_col = 'A', parse_cols = item)
PER = "발표 PER"
PBR = "발표 PBR"
PCR = "과거 PCR"
PSR = "발표 PSR"
GPA ="과거 GP/A (%)"
주가 = '주가 (원)'
부채 = '단순 부채비율 (%)'
모멘텀_1년 = "1년 등락율 (%)"
모멘텀_6개월 = "6개월 등락율 (%)"
모멘텀_3개월 = "3개월 등락율 (%)"
모멘텀_1개월 = "1개월 등락률 (%)"
거래대금 = "거래대금 (20일평균 억)"
FILE = 'quantking191022.xlsx'
FILENAME = "200627_슈퍼가치 가치지표 우선 선별 소형주20퍼이하 부채비율100, 20개 from 191022"
FILE_SAVE = "{FILENAME}_포트.xlsx".format(FILENAME=FILENAME)
FILE_backtest = "{FILENAME}_backtest.xlsx".format(FILENAME=FILENAME)

data = pd.read_excel(FILE,index_col = 0 )
data["시가총액/ebitda"] = data['시가총액 (억)']/data['EBITDA (억)']

#스팩 제거
for item in data.index:
    if data["업종 (소)"][item] == "스팩":
        data=data.drop([item])
print('총 종목 수')
print(len(data.index))
#중국 주식 제거
for item in data.index:
    if item[1] == "9":
        data=data.drop([item])
print('중국주식 제거후 종목수 ')
print(len(data.index))

#data = data[data[모멘텀_6개월]>0] #모멘텀 효과 확인
'''print('6개월 모멘텀>0 선별후')
모멘텀6개월 = len(data.index)
print(len(data.index), 모멘텀6개월/총종목)'''

# PBR 0.2 이하 제외, 시가총액 하위 20%
data = data[data[PBR]>0.2]
print('pbr>0.2 선별후')
print(len(data.index))
data = data[data[PSR]>0.000001]
print('psr>0 선별후')
print(len(data.index))
data = data[data[PCR]>0.0000001]
print('pcr>0 선별후')
print(len(data.index))
data = data[data[PER]>0.000001]
print('per>0 선별후')
print(len(data.index))

#시가총액 하위 20퍼
data = ltoh_percent(data, '시가총액 (억)', 20)
print('시가총액 50퍼 선별후')
print(len(data.index))
#거래대금 5000만원 이상_ 거래대금이 높아야 슬리피지 위험 줄일수 있겠지?
data = data[data[거래대금]>0.1]
print('거래대금 1천 이상 선별후')
print(len(data.index))
#부채비율
#data = data[data[부채]<75]
data = data[data[부채]<100]
print('부채 100이하 선별후')
print(len(data.index))
#data = data[data[부채]>20]
# PBR 0.2 이하 제외, 시가총액 하위 20%
'''data = data[data[PBR]>0.2]
print('pbr>0.2 선별후')
print(len(data.index))
data = data[data[PSR]>0.000001]
print('psr>0 선별후')
print(len(data.index))'''
#data = data[data[PCR]>0.0000001]
#print('pcr>0 선별후')
#print(len(data.index))
#data = data[data[PER]>0.000001]
#print('per>0 선별후')

#print('가치지수 양호 ')
#print(len(data.index))
#모멘텀 >0
#data = data[data[모멘텀_1년]>0]
#data = data[data[모멘텀_6개월]>0]
#data = data[data[모멘텀_3개월]>0]
#data = data[data[모멘텀_1개월]>0]


#newdata = thinning_data_des(newdata, 주가, 150000)


PBR_rank = data[PBR].rank(axis=0)
PER_rank = data[PER].rank(axis=0)
PSR_rank = data[PSR].rank(axis=0)
PCR_rank = data[PCR].rank(axis=0)
sum_가치_rank = (PBR_rank+PER_rank+PSR_rank+PCR_rank).rank(axis=0)
모멘텀_1년_rank = data[모멘텀_1년].rank(axis=0, ascending = False)
모멘텀_6개월_rank = data[모멘텀_6개월].rank(axis=0, ascending = False)
모멘텀_1개월_rank = data[모멘텀_1개월].rank(axis=0, ascending = False)
sum_모멘텀_rank = (모멘텀_1년_rank).rank(axis=0)

sum_rank = (sum_가치_rank + 0*sum_모멘텀_rank).rank(axis =0)
sum_rank = sum_rank.sort_values()

data.insert(len(data.columns),"PBR_rank",PBR_rank)
data.insert(len(data.columns),"PER_rank",PER_rank)
data.insert(len(data.columns),"PSR_rank",PSR_rank)
data.insert(len(data.columns),"PCR_rank",PCR_rank)
data.insert(len(data.columns),"가치_rank",sum_가치_rank)
data.insert(len(data.columns),"모멘텀_rank",sum_모멘텀_rank)
data.insert(len(data.columns),"total rank",sum_rank)


#data = data[data[모멘텀_6개월]>-10] #모멘텀 효과 확인

'''newdata.insert(1,"PBR_rank",PBR_rank)
newdata.insert(1,"GP/A-rank",GPA_rank)
newdata.insert(1,"total rank",sum_rank)'''
data = data.sort_values(by=['total rank'])

data.to_excel(FILE_SAVE, "w")


stocklist = data.head(10).index.tolist()
for i in range(0,len(stocklist)):
    stocklist[i]=stocklist[i].replace("A","")

#data11 = 변동성_naver(stocklist,240,30)
month_data = month_naver_fromto(stocklist,1,18)
data1 = back_test(month_data, 0) #cash ratio:0-1.0
data1.to_excel(FILE_backtest, "w")