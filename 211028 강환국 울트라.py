#이익모멘텀 이용
import pandas as pd
from pandas import Series, DataFrame
from quant_functions import thinning_data_asc, thinning_data_des
from quant_functions import *
from DBUpdater import *
import matplotlib.pyplot as plt
import datetime
#DataBase update

db = DBUpdater()
db.update_comp_info()
db.update_daily_price(5)


# 시가총액 하위 10%
 #  data = pd.read_excel('test.xlsx', idex_col = 'A', parse_cols = item)
start_day = '2021-12-09'
PER = "발표 분기 PER"
#PER = "발표 PER"
PBR = "발표 PBR"
PCR = "과거 PCR"
PSR = "과거 PSR"
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
순이익QOQ = "순이익 21년3Q QOQ" #순이익QOQ = "순이익 21년2Q(E) QOQ"
순이익YOY = "순이익 21년3Q YOY" #순이익YOY = "순이익 21년2Q(E) YOY"
영업이익QOQ = "영업이익 21년3Q QOQ" #영업이익QOQ = "영업이익 21년2Q(E) QOQ"
영업이익YOY = "영업이익 21년3Q YOY" #영업이익YOY = "영업이익 21년2Q(E) YOY"
자산증가율 = '자산증가율 (최근분기)'
주가변동성 = '주가 변동성'
거래대금 = "거래대금 (20일평균 억)"
EV_EBITDA = "과거 EV/EBITDA (%)"
시총EBITDA = "시가총액/ebitda"
FILE = 'quantking220323.csv' #직전은 211209   #181026, 191022등으로 back test 가능
FILEdate = FILE[9:15]
종목수 = 20
시가총액하위 = 20 #시가총액 하위 퍼센또
FILENAME = "211221_울트라, 선별 소형주{시가총액하위} 퍼이하, {종목수} 개 from {FILEdate}".format(FILEdate=FILEdate,종목수 = 종목수,시가총액하위=시가총액하위) # per이나 ev나 크게 상관없는것으로 보임..
FILE_SAVE = "{FILENAME}_포트.xlsx".format(FILENAME=FILENAME)
FILE_backtest = "{FILENAME}_backtest.xlsx".format(FILENAME=FILENAME)
FILE_backtest = "{FILENAME}_backtest.xlsx".format(FILENAME=FILENAME)
ev=0;가치=1;모멘텀=1;gpa=0

data = pd.read_csv(FILE,index_col = 0 )
#data = pd.read_excel(FILE,index_col = 0 )
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
#시가총액 하위
data = ltoh_percent(data, '시가총액 (억)', 시가총액하위)
#data = data[data['시가총액 (억)']<550] #시가 총액 10%는 너무 작아서..
print('시가총액 {시가} 선별후'.format(시가=시가총액하위))
print(len(data.index))

#금융주 제거
data= data[data['업종 (대)']!='금융']
print('금융주 제거후')
print(len(data.index))


# PBR 0.2 이하 제외, 시가총액 하위 20%
data = data[data[PBR]>0.2]
print('pbr 선별후')
print(len(data.index))
data = data[data[PSR]>0.]
print('psr 선별후')
print(len(data.index))
data = data[data[PER]>0.]
print('per 선별후')
print(len(data.index))
data = data[data[PFCR]>0.]
print('pfcr 선별후')
print(len(data.index))

#Fscore
data = data[data['F스코어 지배주주순익>0 여부']>0.5]
print(f'F score 지배주주순익>0 후 {len(data.index)}')
data = data[data['F스코어 영업활동현금흐름>0 여부']>0.5]
print(f'F score 영업활동현금흐름>0 후 {len(data.index)}')
#data = data[data['F스코어 신주발행X 여부']>0.5]
#print(f'F score 신주발행x 후 {len(data.index)}')

#관리종목 제외
data = data[data['관리 종목 =1']!=1]
print('관리종목 제거후')
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
GPA_rank = data[GPA].rank(axis=0, ascending = False)
자산증가율_rank = data[자산증가율].rank(axis=0)
주가변동성_rank = data[주가변동성].rank(axis=0)
시총EBITDA_rank = data[시총EBITDA].rank(axis=0) # ev 대신 시가총액 사용
PBR_rank = data[PBR].rank(axis=0)
PER_rank = data[PER].rank(axis=0)
PSR_rank = data[PSR].rank(axis=0)
PFCR_rank = data[PFCR].rank(axis=0)
#sum_가치_rank = (PER_rank+PBR_rank+PSR_rank+PCR_rank).rank(axis=0) #PER 지표 안쓰고
순이익YOY_rank = data[순이익YOY].rank(axis=0, ascending = False)
순이익QOQ_rank = data[순이익QOQ].rank(axis=0, ascending = False)
영업이익YOY_rank = data[영업이익YOY].rank(axis=0, ascending = False)
영업이익QOQ_rank = data[영업이익QOQ].rank(axis=0, ascending = False)

sum_rank = (GPA_rank + 자산증가율_rank+주가변동성_rank+ 가치*(PER_rank+PBR_rank+PSR_rank+PFCR_rank)+모멘텀*(순이익YOY_rank+순이익QOQ_rank+영업이익YOY_rank+영업이익QOQ_rank)).rank(axis =0)
sum_rank = sum_rank.sort_values()
data.insert(len(data.columns),"total rank",sum_rank)


#data = data[data[모멘텀_6개월]>-10] #모멘텀 효과 확인

'''newdata.insert(1,"PBR_rank",PBR_rank)
newdata.insert(1,"GP/A-rank",GPA_rank)
newdata.insert(1,"total rank",sum_rank)'''
data = data.sort_values(by=['total rank'])
data.to_excel(FILE_SAVE, "w")

#해당 포트폴리오의 추세확인
stocklist = data.head(종목수).index.tolist()
for i in range(0,len(stocklist)):
    stocklist[i]=stocklist[i].replace("A","")
price_list = MarketDB()
today = datetime.datetime.now().strftime('%Y-%m-%d')
stk_price = price_list.get_daily_price_list(stocklist,start_date=start_day,end_date=today)

print(stk_price)
stk_price_수익 = stk_price/stk_price.iloc[0]
stk_price_수익['전체평균수익'] = stk_price_수익.mean(axis=1)
#stk_price_수익.to_excel(f"{today}, 울트라 전략 확인.xlsx")
stk_price_수익['MA10'] = stk_price_수익['전체평균수익'].rolling(window=12).mean()
stk_price_수익['MA20'] = stk_price_수익['전체평균수익'].rolling(window=26).mean()
stk_price_수익['MA60'] = stk_price_수익['전체평균수익'].rolling(window=60).mean()
stk_price_수익['MACD'] = stk_price_수익['전체평균수익'].rolling(window=12).mean()-stk_price_수익['전체평균수익'].rolling(window=26).mean()
stk_price_수익['MACD_signal'] = stk_price_수익['MACD'].rolling(window=9).mean()
stk_price_수익['MACD_osc'] = stk_price_수익['MACD']-stk_price_수익['MACD_signal']
stk_price_수익['pc_upper'] = stk_price_수익['전체평균수익'].rolling(window=20).max().shift(1)
stk_price_수익['pc_lower'] = stk_price_수익['전체평균수익'].rolling(window=10).min().shift(1)


plt.figure(figsize=(18,14))
p1 = plt.subplot(2,1,1)
plt.title('first screen_price moving')
plt.rc('font', size=20)
plt.plot(stk_price_수익.index, stk_price_수익['전체평균수익'],marker='o',markersize=5, label='return avg', linewidth=3, color='gray')
plt.plot(stk_price_수익.index, stk_price_수익['MA10'], color = 'red',label='MA12')
plt.plot(stk_price_수익.index, stk_price_수익['MA20'], color = 'orange',label='MA26')
plt.plot(stk_price_수익.index, stk_price_수익['MA60'], color = 'blue',label='MA60')
plt.plot(stk_price_수익.index, stk_price_수익['pc_upper'], color = 'green',label='pc_upper')
plt.plot(stk_price_수익.index, stk_price_수익['pc_lower'], color = 'green',label='pc_lower')
plt.grid(True)
plt.legend()
plt.xlim([stk_price_수익.index[0],stk_price_수익.index[-1]+datetime.timedelta(days=20)])
p2 = plt.subplot(2,1,2)
plt.grid(True)
plt.bar(stk_price_수익.index,stk_price_수익['MACD_osc'], color='m',label='MACD-HIST')
plt.plot(stk_price_수익.index,stk_price_수익['MACD'], color='black',label='MACD')
plt.plot(stk_price_수익.index,stk_price_수익['MACD_signal'],'g--',label='MACD-Signal')
plt.xlim([stk_price_수익.index[0],stk_price_수익.index[-1]+datetime.timedelta(days=20)])
'''
stocklist = data.head(종목수).index.tolist()
for i in range(0,len(stocklist)):
    stocklist[i]=stocklist[i].replace("A","")

#data11 = 변동성_naver(stocklist,240,30)
#month_data = month_naver_fromto(stocklist,24,52)


from quant_functions import *
month_data = month_naver_fromto_better(stocklist,'2021-07-22','2021-09-26')

data1 = back_test(month_data, 0) #cash ratio:0-1.0
data1.to_excel(FILE_backtest, "w")
'''