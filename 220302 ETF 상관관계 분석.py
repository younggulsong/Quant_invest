from pykrx import stock  #https://defineall.tistory.com/746
import pykrx
from Investstrategy import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df1 = stock.get_market_ohlcv_by_date("20181021", "20220104", "122630")['종가']
df2 = stock.get_market_ohlcv_by_date("20181021", "20220104", "122630")['종가']


df = pd.DataFrame()
ETFlist = pd.read_excel('220302_ETF리스트.xlsx')
#filter
ETFlist = ETFlist[ETFlist['총보수']<=0.3] #총보수 작은거 (<0.3%)
ETFlist = ETFlist[ETFlist['추적배수']=='일반 (1)'] #총보수 작은거 (<0.3%)


ETF_code = pd.DataFrame()
ETF_code = ETFlist['한글종목약명']
ETF_code.index = ETFlist['단축코드']

etf_data = pd.DataFrame()
etf_수익률 = pd.DataFrame()
total = len(ETF_code)
#3,6,9,12,24,36 개월 수익 확인하기
etf_수익률.index= ETF_code
etf_수익률[['1개월','3개월','6개월','12개월','24개월','36개월']] = 1.
for i, code in enumerate(ETF_code.index):
    code = str(code).zfill(6)  # 5자리를 6자리로 만들기
    print(f"{i}/{total}", code, ETF_code.iloc[i])
    df = stock.get_market_ohlcv_by_date("20181021", "20220409", code)['종가']
    etf_수익률.loc[ETF_code.iloc[i],'1개월'] = (df/df.shift(20))[-1].round(4)-1
    etf_수익률.loc[ETF_code.iloc[i],'3개월'] = (df/df.shift(60))[-1].round(4)-1
    etf_수익률.loc[ETF_code.iloc[i],'6개월'] = (df/df.shift(120))[-1].round(4)-1
    etf_수익률.loc[ETF_code.iloc[i],'12개월'] = (df/df.shift(240))[-1].round(4)-1
    etf_수익률.loc[ETF_code.iloc[i],'24개월'] = (df/df.shift(480))[-1].round(4)-1
    etf_수익률.loc[ETF_code.iloc[i],'36개월'] = (df/df.shift(720))[-1].round(4)-1
etf_수익률.to_excel('220409_ETF_수익률.xlsx')

#corr 구하기 위한 시계열 수집
for i, code in enumerate(ETF_code.index):
    code = str(code).zfill(6) #5자리를 6자리로 만들기
    print(f"{i}/{total}", code, ETF_code.iloc[i])
    df = stock.get_market_ohlcv_by_date("20161021", "20220409", code)['종가']
    df.name = ETF_code.iloc[i]
    df = df/df.shift(1)
    etf_data= pd.concat([etf_data,df],axis=1)

corr_ETF = etf_data.corr()
corr_ETF.to_excel('220319_ETFcorr.xlsx')

plt.figure(figsize=(8, 6))
sns.heatmap(corr_ETF, annot=True)
plt.show()