import pandas as pd
from pandas import Series, DataFrame
from quant_functions import thinning_data_asc, thinning_data_des
from quant_functions import *

# 시가총액 하위 10%
 #  data = pd.read_excel('test.xlsx', idex_col = 'A', parse_cols = item)
PER = "발표 분기 PER"
PER = "발표 PER"
PBR = "발표 PBR"
PCR = "과거 PCR"
PSR = "발표 PSR"
PFCR = "과거 PFCR"
POR =  "발표 POR"
GPA ="과거 GP/A (%)"
주가 = '주가 (원)'
부채 = '단순 부채비율 (%)'
차입금비율 = '차입금 비율 (%)'
모멘텀_1년 = "1년 등락률 (%)"
모멘텀_9개월 = "9개월 등락률 (%)"
모멘텀_6개월 = "6개월 등락률 (%)"
모멘텀_3개월 = "3개월 등락률 (%)"
모멘텀_1개월 = "1개월 등락률 (%)"
거래대금 = "거래대금 (20일평균 억)"
EV_EBITDA = "과거 EV/EBITDA (%)"
시총EBITDA = "시가총액/ebitda"
NCAV = "청산가치비율 (NCAV전략) (%)"
Fscore = "F스코어 점수 (9점만점)"
FILE = 'quantking201126.xlsx'   #181026, 191022등으로 back test 가능
FILEdate = FILE[9:15]
종목수 = 20
시가총액하위 = 20 #시가총액 하위 퍼센또
FILENAME = "201126_NCAV,GPA전력 {종목수} 개 from {FILEdate}".format(FILEdate=FILEdate,종목수 = 종목수,시가총액하위=시가총액하위) # per이나 ev나 크게 상관없는것으로 보임..
FILE_SAVE = "{FILENAME}_포트.xlsx".format(FILENAME=FILENAME)
FILE_backtest = "{FILENAME}_backtest.xlsx".format(FILENAME=FILENAME)
ev=0;가치=1;모멘텀=1;gpa=0

data = pd.read_excel(FILE,index_col = 0 )
data["시가총액/ebitda"] = data['시가총액 (억)']/data['EBITDA (억)'] #시총/EBITDA




#스팩 제거
for item in data.index:
    if data["업종 (소)"][item] == "스팩":
        data=data.drop([item])
print('스팩 제거후')
print(len(data.index))
#지주사 제거
for item in data.index:
    if data["업종 (소)"][item] == "지주사":
        data=data.drop([item])

print('지주사 제거후')
print(len(data.index))

#금융주 제거
for item in data.index:
    if data["업종 (대)"][item] == "금융":
        data=data.drop([item])

print('금융주 제거후')
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


#거래대금 생각안하고..
#data = data[data[거래대금]>0.1]
#print('거래대금 1천 이상 선별후')
#print(len(data.index))
#부채비율
#data = data[data[부채]<75]
data = data[data[차입금비율]<200]
print('차입금 비율 200%이하 선별후')
print(len(data.index))

#시가총액 하위
'''data = ltoh_percent(data, '시가총액 (억)', 시가총액하위)
print('시가총액 {시가} 선별후'.format(시가=시가총액하위))
print(len(data.index))'''


# PBR 0.2 이하 제외, 시가총액 하위 20%
'''data = data[data[PBR]>0.2]
print('pbr 선별후')
print(len(data.index))
data = data[data[PSR]>0.1]
print('psr 선별후')
print(len(data.index))
data = data[data[PCR]>1.]
print('pcr 선별후')
print(len(data.index))
data = data[data[PER]>2.]
print('per 선별후')
print(len(data.index))
data = data[data[PFCR]>1.]
print('pfcr 선별후')
print(len(data.index))
data = data[data[POR]>2.]
print('por 선별후')
print(len(data.index))
data = data[data[모멘텀_1년]<70]
data = data[data[모멘텀_9개월]<70]
data = data[data[모멘텀_6개월]<70]
data = data[data[모멘텀_3개월]<70]
data = data[data[모멘텀_1개월]<70]
print('모멘텀 70%이하 선별')
print(len(data.index))'''

data = data[data[PER]>0.]
print('per 선별후')
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
GPA_rank = data[GPA].rank(axis=0,ascending = False)
NCAV_rank = data[NCAV].rank(axis=0,ascending = False)
F_rank = data[Fscore].rank(axis=0,ascending = False)
'''시총EBITDA_rank = data[시총EBITDA].rank(axis=0) # ev 대신 시가총액 사용
PBR_rank = data[PBR].rank(axis=0)
PER_rank = data[PER].rank(axis=0)
PSR_rank = data[PSR].rank(axis=0)
PCR_rank = data[PCR].rank(axis=0)
POR_rank = data[POR].rank(axis=0)
PFCR_rank = data[PFCR].rank(axis=0)
EV_rank = data[EV_EBITDA].rank(axis=0)
sum_가치_rank = (PER_rank+PBR_rank+PSR_rank+PCR_rank).rank(axis=0) #PER 지표 안쓰고
모멘텀_1년_rank = data[모멘텀_1년].rank(axis=0, ascending = False)
모멘텀_9개월_rank = data[모멘텀_9개월].rank(axis=0, ascending = False)
모멘텀_6개월_rank = data[모멘텀_6개월].rank(axis=0, ascending = False)
모멘텀_3개월_rank = data[모멘텀_3개월].rank(axis=0, ascending = False)
모멘텀_1개월_rank = data[모멘텀_1개월].rank(axis=0, ascending = False)
sum_모멘텀_rank = (모멘텀_1년_rank).rank(axis=0)'''

sum_rank = (GPA_rank + NCAV_rank).rank(axis =0)
sum_rank = sum_rank.sort_values()


data.insert(len(data.columns),"NCAV_rank",NCAV_rank)
data.insert(len(data.columns),"GPA_rank",GPA_rank)
data.insert(len(data.columns),"Fscore_rank",F_rank)
data.insert(len(data.columns),"total rank",sum_rank)


#data = data[data[모멘텀_6개월]>-10] #모멘텀 효과 확인

'''newdata.insert(1,"PBR_rank",PBR_rank)
newdata.insert(1,"GP/A-rank",GPA_rank)
newdata.insert(1,"total rank",sum_rank)'''
data = data.sort_values(by=['total rank'])

data.to_excel(FILE_SAVE, "w")

stocklist = data.head(종목수).index.tolist()
for i in range(0,len(stocklist)):
    stocklist[i]=stocklist[i].replace("A","")

#data11 = 변동성_naver(stocklist,240,30)
#month_data = month_naver_fromto(stocklist,24,52)

from quant_functions import *
month_data = month_naver_fromto_better(stocklist,'2020-08-22','2020-11-22')

data1 = back_test(month_data, 0) #cash ratio:0-1.0
data1.to_excel(FILE_backtest, "w")
