from pandas import Series, DataFrame
import requests
from bs4 import BeautifulSoup
import pandas as pd


def thinning_data_asc(data, metric, value):
    data = data.sort_values(by=[metric], ascending=True)
    for code in data.index:
        if data[metric][code] < value:
            data = data.drop([code])
        else:
            break
    return data
def thinning_data_des(data, metric, value):
    data = data.sort_values(by=[metric], ascending=False)
    for code in data.index:
        if data[metric][code] > value:
            data = data.drop([code])
        else:
            break
    return data

def ltoh_percent(data, metric, percent):
    data = data.sort_values(by=[metric],ascending=True)
    number_remain = int(len(data.index)*percent/100)
    print(number_remain)
    newdata = DataFrame(data.head(number_remain), copy=False)
    return newdata
def htol_percent(data, metric, percent):
    data = data.sort_values(by=[metric],ascending=False)
    number_remain = int(len(data.index)*percent/100)
    print(number_remain)
    newdata = DataFrame(data.head(number_remain), copy=False)
    return newdata

def test():
    data = DataFrame()
    return data

#month_naver는 해당 종목코드 리스트를 받아서 이에 대한 월별 데이터를 순차적으로 모아놓는 함수다.
def month_naver(itemlist, pages):  ## Reference : http://excelsior-cjh.tistory.com/109
    data = DataFrame()
    j=1
    for code in itemlist:
        print(code,j)
        j+=1
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
        # dataframe 정의
        df = DataFrame()

        for page in range(1, pages + 1):
            pg_url = '{url}&page={page}'.format(url=url, page=page)
            df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
        df=df.dropna(axis=0) # nan이 있는 행 지우기
        df = df.reset_index() # 0,1,2,3,4, 재인덱싱

        df_month = Series()
        i = 0
        for dates in df["날짜"].values:
            if i % 20 == 0:
                df_month.loc[dates] = df.loc[i]["종가"]
                i += 1
            else:
                i += 1

        df_month.index = pd.to_datetime(df_month.index)
        data.insert(len(data.columns), code, df_month)
    return data

def month_naver_fromto(itemlist, start_page, pages):  ## Reference : http://excelsior-cjh.tistory.com/109
    data = DataFrame()
    j=1
    for code in itemlist:
        print(code,j)
        j+=1
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
        # dataframe 정의
        df = DataFrame()

        for page in range(start_page, pages + 1):
            pg_url = '{url}&page={page}'.format(url=url, page=page)
            df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
        df=df.dropna(axis=0) # nan이 있는 행 지우기
        df = df.reset_index() # 0,1,2,3,4, 재인덱싱

        df_month = Series()
        i = 0
        for dates in df["날짜"].values:
            if i % 20 == 0:
                df_month.loc[dates] = df.loc[i]["종가"]
                i += 1
            else:
                i += 1

        df_month.index = pd.to_datetime(df_month.index)
        data.insert(len(data.columns), code, df_month)
    return data

def back_test(data_month, cash_ratio):
    print("test")
    data = DataFrame(data_month, copy=True)
    items = data.columns
    item_count = len(items)

    평가금액 = 1.
    주식매수 = 평가금액 * (1 - cash_ratio)
    현금 = 평가금액 * cash_ratio
    주당투자 = 주식매수 / item_count


    for item in items:
        data.insert(len(data.columns), "주가수익({item})".format(item=item), 1.)
    for item in items:
        data.insert(len(data.columns), "종목리밸런싱({item})".format(item=item),주당투자)
    data.insert(len(data.columns), "현금", 현금)
    data.insert(len(data.columns), "총합계", 1.1)
    data.insert(len(data.columns), "단순합계", 1.1)

    data = data.sort_index()  # sort_index : index로 dataframe sorting 시간에 따라 sorting하려고

    date_bef = data.index[0]
    for date in data.index:

        for item in items:
            data["주가수익({item})".format(item=item)][date] = data["주가수익({item})".format(item=item)][date_bef] * (data[item][date])/(data[item][date_bef])
            data["종목리밸런싱({item})".format(item=item)][date] = data["종목리밸런싱({item})".format(item=item)][date_bef] * (data[item][date])/(data[item][date_bef])
        sum = 0
        단순합=0
        for item in items:
            sum = sum + data["종목리밸런싱({item})".format(item=item)][date]
            단순합= 단순합 + data["주가수익({item})".format(item=item)][date]
        newstocksum = (sum+data["현금"][date_bef]) * (1-cash_ratio)
        data["현금"][date] = (sum+data["현금"][date_bef]) * cash_ratio
        data["총합계"][date] = sum+data["현금"][date_bef]
        data["단순합계"][date] = 단순합/item_count
        for item in items:
            data["종목리밸런싱({item})".format(item=item)][date] = newstocksum/item_count

        date_bef = date
        

    return data

def 변동성_naver(itemlist, time, days):  ## Reference : http://excelsior-cjh.tistory.com/109
    ## 1년전 한달동안 변동성
    data = DataFrame()
    time_pages = (time-1)//10+1
    days_pages = (days-1)//10+1
    df_std=Series()
    df_avg=Series()
    df_rel=Series()
    j=1

    for code in itemlist:
        print(code,j)
        j+=1
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
        # dataframe 정의
        df = DataFrame()

        for page in range(time_pages, time_pages + days_pages + 1):
            pg_url = '{url}&page={page}'.format(url=url, page=page)
            df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
        df=df.dropna(axis=0) # nan이 있는 행 지우기
        df = df.reset_index() # 0,1,2,3,4, 재인덱싱

        df_std[code]=df["종가"].std()
        df_avg[code]=df["종가"].mean()
        df_rel[code] = 100*df["종가"].std()/df["종가"].mean()

    data.insert(len(data.columns), "avg", df_avg)
    data.insert(len(data.columns), "std", df_std)
    data.insert(len(data.columns), "rel", df_rel)

    return data

def day_naver_fromto(itemlist, start_page, pages):  ## Reference : http://excelsior-cjh.tistory.com/109
    data = DataFrame()
    j=1
    for code in itemlist:
        print(code,j)
        j+=1
        #url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
        url = 'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSPI'

        df = DataFrame()

        for page in range(start_page, pages + 1):
            pg_url = '{url}&page={page}'.format(url=url, page=page)
            df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
        df=df.dropna(axis=0) # nan이 있는 행 지우기
        df = df.reset_index() # 0,1,2,3,4, 재인덱싱

        df_month = Series()
        i = 0
        for dates in df["날짜"].values:
            if i % 1 == 0:
                df_month.loc[dates] = df.loc[i]["종가"]
                i += 1
            else:
                i += 1

        df_month.index = pd.to_datetime(df_month.index)
        data.insert(len(data.columns), code, df_month)
    return data

def month_naver_fromto_better(itemlist, date_st,date_end):  ## Reference : http://excelsior-cjh.tistory.com/109
    data = DataFrame()
    j=1
    for code in itemlist:
        print(code,j)
        j+=1
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
        # dataframe 정의
        df = DataFrame()

        df = get_price(code,date_st,date_end)
        df_month = Series()
        i = 0
        for date in df.index:
            if i % 20 == 0:
                df_month.loc[date] = df['Close'][date]
                i += 1
            else:
                i += 1

        df_month.index = pd.to_datetime(df_month.index)
        data.insert(len(data.columns), code, df_month)
    return data

def get_price(company_code, date_st, date_end):
    # count=3000에서 3000은 과거 3,000 영업일간의 데이터를 의미. 사용자가 조절 가능
    url = "https://fchart.stock.naver.com/sise.nhn?symbol={}&timeframe=day&count=3000&requestType=0".format(
        company_code)
    get_result = requests.get(url)
    bs_obj = BeautifulSoup(get_result.content, "html.parser")

    # information
    inf = bs_obj.select('item')
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df_inf = pd.DataFrame([], columns=columns, index=range(len(inf)))

    for i in range(len(inf)):
        df_inf.iloc[i] = str(inf[i]['data']).split('|')

    df_inf.index = pd.to_datetime(df_inf['Date'])
    df_inf = df_inf.drop('Date', axis=1).astype(float)

    df_inf = df_inf[date_st:date_end]
    return df_inf
