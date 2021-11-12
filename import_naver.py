## Reference : http://excelsior-cjh.tistory.com/109
import urllib
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt

from urllib.request import urlopen
from bs4 import BeautifulSoup

#종목이름 입력하면 종목에 해당하는 코드를 불러와 네이버 금융에 넣어준다.
def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)

    print("요청 URL = {}".format(url))
    return url

item_name = '신라젠'
code_df = 215600
url = 'http://finance.naver.com/item/sise_day.nhn?code=000660'

# dataframe 정의
df = pd.DataFrame()

for page in range(1,50):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    df = df.append(pd.read_html(pg_url,header =0)[0], ignore_index=True)

df = df.dropna()
df_month = pd.Series()
i=0
for dates in df["날짜"].values:
    if i%20 ==0:
        print(i)
        df_month.loc[dates]=df.loc[i]["종가"]
        i+=1
    else:
        i+=1

df["날짜"] = pd.to_datetime(df["날짜"])
df_month.index = pd.to_datetime(df_month.index)
plt.plot(df_month.index,df_month, label = "주가")
plt.legend(loc='best')
plt.grid()