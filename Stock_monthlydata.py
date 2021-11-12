import pandas as pd
from pandas import Series, DataFrame
from time import sleep
from quant_functions import *

 #  data = pd.read_excel('test.xlsx', idex_col = 'A', parse_cols = item)

FILE = 'test.xlsx'
FILE_SAVE = "180725_monthly_stock.xlsx"
data = pd.read_excel(FILE,index_col = 0 )

#스팩 제거
for item in data.index:
    if data["업종\n(소)"][item] == "스팩":
        data=data.drop([item])

stocklist = data.index.tolist()
for i in range(0,len(stocklist)):
    stocklist[i]=stocklist[i].replace("A","")

result = DataFrame()
'''j=200
for i in range(1,10):
    print(i*j,"-",i*j+j)
    splitlist = stocklist[i*j:i*j+j]
    month_data = month_naver_fromto(splitlist,1,32)
    result = pd.concat([result, month_data],axis=1)
    sleep(1200)
'''
result = month_naver_fromto(stocklist,1,10)
result.to_excel("180725_monthly_stock_.xlsx", "w")