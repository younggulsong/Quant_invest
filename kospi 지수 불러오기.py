import pandas as pd
from pandas import Series, DataFrame
start_page=1
pages=600
        #url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
        url = 'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSPI'

        df = DataFrame()
    i=1
        for page in range(start_page, pages + 1):
            pg_url = '{url}&page={page}'.format(url=url, page=page)
            df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
            print(i)
            i+=1
        df=df.dropna(axis=0) # nan이 있는 행 지우기
        df = df.reset_index() # 0,1,2,3,4, 재인덱싱

df.to_excel("kospi지수.xlsx","w")

        df_month.index = pd.to_datetime(df_month.index)
        data.insert(len(data.columns), code, df_month)
