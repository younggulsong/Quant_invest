import pandas as pd
from pandas import Series, DataFrame

data = DataFrame(df_month, columns= ["주가"])

data.insert(len(data.columns), "주가수익",1.1)
data.insert(len(data.columns), "리밸런싱",1.1)
data.insert(len(data.columns), "현금",1.1)
data.insert(len(data.columns), "총합계",1.1)
data = data.sort_index() #sort_index : index로 dataframe sorting

평가금액 = 1.
주식매수 = 평가금액 * 0.5
현금 = 평가금액 * 0.5
date_bef = data.index[0]
for date in data.index:

    평가금액 = 평가금액 * (data["주가"][date]) / (data["주가"][date_bef])
    주식매수 = 주식매수 * (data["주가"][date]) / (data["주가"][date_bef])
    주식매수 = (주식매수 + 현금) * 0.5
    현금 = 주식매수 * (1-0.5)/0.5
    data["주가수익"][date]= 평가금액
    data["리밸런싱"][date] = 주식매수
    data["현금"][date] = 현금
    data["총합계"][date] = 현금+주식매수
    date_bef = date