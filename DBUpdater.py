'''
class DBUpdater:
    def __init__(self):

    def __del__(self):

    def read_krx_code(self):

    def update_comp_info(self):

    def read_naver(self,code, company, pages_to_fetch):

    def replace_into_db(self,df,num,code,company):

    def update_daily_price(self, pages_to_fetch):

    def execute_daily(self):


if __name__=='__main__':
    dbu=DBUpdater()
    dbu.execute_daily()
    ''' #연습

import pandas as pd
from bs4 import BeautifulSoup
import urllib, pymysql, calendar, time, json
from urllib.request import urlopen
from datetime import datetime, timedelta
from threading import Timer
from pandas import Series, DataFrame
import requests
import re


class DBUpdater:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root',
                                    password='#dudrjf1380', db='INVESTAR', charset='utf8')

        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS company_info (
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (code))
            """
            curs.execute(sql)
            sql = """
            CREATE TABLE IF NOT EXISTS daily_price (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            """
            curs.execute(sql)
        self.conn.commit()
        self.codes = dict()

    def read_krx_code(self):
        """KRX로부터 상장기업 목록 파일을 읽어와서 데이터프레임으로 반환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=' \
              'download&searchType=13'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
        krx.code = krx.code.map('{:06d}'.format)
        return krx

    def update_comp_info(self):
    #종목 코드를 company_info 테이블에 업데이트한 후 딕셔너리에 저장
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql,self.conn)

        for idx in range(len(df)):# 코드번호와 회사 이름을 연결하는 딕셔너리만들기.
            self.codes[df['code'].values[idx]]=df['company'].values[idx]

        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info" #DB에서 가장 최근 업데이트날짜를 가져옴
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')
             # 오늘보다 오래된 경우에만 업데이트
            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                krx = self.read_krx_code()
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]
                    sql = f"REPLACE INTO company_info (code, company, last_update) VALUES ('{code}', '{company}', '{today}')"
                    curs.execute(sql)
                    self.codes[code] = company # codes 딕셔너리 update
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] #{idx + 1:04d} REPLACE INTO company_info " \
                          f"VALUES ({code}, {company}, {today})")

                self.conn.commit()
                print('')

    def read_naver(self, code, dates):
        try:
            url = "https://fchart.stock.naver.com/sise.nhn?symbol={}&timeframe=day&count={}&requestType=0".format(
                code,dates)
            get_result = requests.get(url)
            bs_obj = BeautifulSoup(get_result.content, "html.parser")
            # information
            inf = bs_obj.select('item')
            columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            df_inf = pd.DataFrame([], columns=columns, index=range(len(inf)))

            for i in range(len(inf)):
                df_inf.iloc[i] = str(inf[i]['data']).split('|')
            df_inf['date'] = pd.to_datetime(df_inf['date'])

        except Exception as e:
            print('Exception occured:', str(e))
            return None
        return df_inf

    def replace_into_db(self,df,num,code,company):
        """네이버에서 읽어온 주식시세를 DB에 Replace"""
        with self.conn.cursor() as curs:
            for r in df.itertuples():

                sql = "REPLACE INTO daily_price VALUES ('{}','{}',{},{},{},{},{})".format(code,r.date,r.open,r.high,r.low,r.close,r.volume)
                curs.execute(sql)
            self.conn.commit()
            print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_price [OK]'.format(datetime.now().strftime('%Y-%m-%d %H:%M'), num + 1, company, code, len(df)))

    def update_daily_price(self, dates):
        """KRX 상장법인의 주식 시세를 네이버로부터 읽어서 DB에 업데이트"""
        for idx, code in enumerate(self.codes):
            code_num = len(self.codes)
            df = self.read_naver(code, dates)
            if df is None:
                continue
            self.replace_into_db(df, idx, code, self.codes[code])
            print(idx,"/",code_num, " ",code," ",self.codes[code], " updated")

    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

class MarketDB:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root',
                                    password='#dudrjf1380', db='INVESTAR', charset='utf8')
        self.codes = {}
        self.companies = {}
        self.get_comp_info()

    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()
    def get_comp_info(self):
    #종목 코드를 company_info 테이블에 업데이트한 후 딕셔너리에 저장
        sql = "SELECT * FROM company_info"
        krx = pd.read_sql(sql,self.conn)

        for idx in range(len(krx)):  # 코드번호와 회사 이름을 연결하는 딕셔너리만들기.
            self.codes[krx['code'].values[idx]] = krx['company'].values[idx]
            self.companies[krx['company'].values[idx]] = krx['code'].values[idx]


    def get_daily_price(self, code, start_date=None, end_date = None):
        """종목의 일별 시세를 데이터 프레임 형태로 반환"""
        #임의의 날짜 형태를 정규형태로 변화
        start_list = re.split('\D+', start_date)
        end_list = re.split('\D+', end_date)
        start_date = f"{int(start_list[0]):04d}-{int(start_list[1]):02d}-{int(start_list[2]):02d}"
        end_date = f"{int(end_list[0]):04d}-{int(end_list[1]):02d}-{int(end_list[2]):02d}"

        #value가 들어올 경우 key(code)로 변환
        codes_keys = list(self.codes.keys())
        codes_values = list(self.codes.values())
        if code in codes_keys:
            pass
        elif code in codes_values:
            idx = codes_values.index(code)
            code = codes_keys[idx]
        else:
            print("ValueError: Code({}) doesnt exist".format(code))

        #data 불러오기
        sql =f"SELECT * FROM daily_price WHERE code = '{code}' and date >= '{start_date}' and date <= '{end_date}'"
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        df = df.drop(columns='date')
        return df

    def get_daily_price_list(self, codes, start_date=None, end_date=None):
        price_list = DataFrame()

        # value(회사명)이 들어올 경우 key(code)로 변환
        codes_keys = list(self.codes.keys())
        codes_values = list(self.codes.values())
        #데이터 불러와서 합치기
        for code in codes:
            close_prices = self.get_daily_price(code,start_date,end_date)['close']
            price_list.insert(len(price_list.columns),f"{self.codes[code]}",close_prices) #n번째 자리에 self.codes[code]회사명으로 daily prices 기입
        return price_list

'''
prices = MarketDB()
stock_list = ['005930','000660']
stock = prices.get_daily_price('005930',start_date='2019-12-31',end_date='2020-12-31')

stock_price_list = prices.get_daily_price_list(stock_list,start_date='2019-12-31',end_date='2020-12-31')

prices.get_daily_price('삼성전자',start_date='2019-12-31',end_date='2020-12-31')
samsung = prices.get_daily_price('005930',start_date='2019-12-31',end_date='2020-12-31')['close']
hynix = prices.get_daily_price('000660',start_date='2019-12-31',end_date='2020-12-31')['close']

db = DBUpdater()
db.update_comp_info()
db.update_daily_price(30)
'''




'''
list = db.read_naver('005930',300)


company_code = '005930'
dates = 300
url = "https://fchart.stock.naver.com/sise.nhn?symbol={}&timeframe=day&count={}&requestType=0".format(
    company_code, dates)
get_result = requests.get(url)
bs_obj = BeautifulSoup(get_result.content, "html.parser")

# information
inf = bs_obj.select('item')
columns = ['date', 'open', 'high', 'low', 'close', 'volume']
df_inf = pd.DataFrame([], columns=columns, index=range(len(inf)))

for i in range(len(inf)):
    df_inf.iloc[i] = str(inf[i]['data']).split('|')

df_inf.index = pd.to_datetime(df_inf['date'])
df_inf = df_inf.drop('date', axis=1).astype(float)
'''
