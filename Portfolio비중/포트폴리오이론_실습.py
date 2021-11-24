
from DBUpdater import *
import numpy as np
import matplotlib.pyplot as plt
#주식하나 가격부르기 stock = prices.get_daily_price('005930',start_date='2019-12-31',end_date='2020-12-31')
#주식 여러개 종가 모으기 stock_price_list = prices.get_daily_price_list(stock_list,start_date='2019-12-31',end_date='2020-12-31')


stock_list = ['유비벨록스','KBI메탈','한솔로지스틱스','파인디지털','세진티에스','디젠스','삼현철강','진양산업','삼일기업공사','HRS']
price_list = MarketDB()

#code로 리스트 전환
code_list=[]
for name in stock_list:
    code_list.append(price_list.companies[name])

#시계열 구하기
stock_price_list = price_list.get_daily_price_list(code_list,start_date='2010-10-31',end_date='2021-10-31')
days = len(stock_price_list)
print(f"평가기간: 총 {days} 일")
daily_ret = stock_price_list.pct_change() # 일간 수익률
annual_ret = daily_ret.mean()*(2711/246) #연간수익률을 이렇게 산술적으로 곱해도 되나 싶지만 아쉬운데로 따라하기.
daily_cov = daily_ret.cov()
annual_cov = daily_cov *(2711/246)
daily_ret = daily_ret.mean()
matrix = stock_price_list.corr()

port_ret=[]
port_risk=[]
port_weights=[]
sharp_ratio=[]

# N 개의 투자 포트폴리오 생성 (평균은 선형적이나, 포트폴리오 리스크 계산은 비선형적임.)
for _ in range(100000):
    weights = np.random.random(len(stock_list))
    weights /=np.sum(weights)
    returns = np.dot(weights, annual_ret)
    risk = np.sqrt(np.dot(weights.T,np.dot(annual_cov,weights)))
    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)
# 동일 배분
weights = np.ones(len(stock_list))
weights /=np.sum(weights)
returns = np.dot(weights, annual_ret)
risk = np.sqrt(np.dot(weights.T,np.dot(annual_cov,weights)))
port_ret.append(returns)
port_risk.append(risk)
port_weights.append(weights)


portfolio={'returns':port_ret,'risk':port_risk}
for i, s in enumerate(stock_list):
    portfolio[s] = [weight[i] for weight in port_weights]
df = pd.DataFrame(portfolio)
df['sharpe_ratio'] = df['returns']/df['risk']
df = df[['returns','risk','sharpe_ratio']+[s for s in stock_list]] # 이거 왜필요함?

df.plot.scatter(x='risk',y='returns', figsize = (20,14), grid=True)
plt.title('Efficient Frontier')

#max sharpe
max_sharpe = df.loc[df['sharpe_ratio']==df['sharpe_ratio'].max()]
plt.scatter(x=max_sharpe['risk'],y=max_sharpe['returns'],c='r',marker='*',s=500)
#min_risk
min_risk = df.loc[df['risk']==df['risk'].min()]
plt.scatter(x=min_risk['risk'],y=min_risk['returns'],c='r',marker='X',s=500)
#동일 비중
weights = np.ones(len(stock_list))
weights /=np.sum(weights)
returns = np.dot(weights, annual_ret)
risk = np.sqrt(np.dot(weights.T,np.dot(annual_cov,weights)))
plt.scatter(x=risk,y=returns,c='r',marker='v',s=500)

