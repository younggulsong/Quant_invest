#출처: https://engkimbs.tistory.com/625?category=762758
#출처: https://financedata.github.io/posts/naver-finance-finstate-crawling.html
#네이버 재무재표 정보:https://companyinfo.stock.naver.com/company/c1040001.aspx?cmp_cd=005930&cn=
import requests
from bs4 import BeautifulSoup
# 네이버 재무제표 가져오기 연습.. 근데 2017년도글이라그런지 삭제된거 같음

import pandas as pd

url_tmpl= 'http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=%s&fin_typ=%s&freq_typ=%s'
url = url_tmpl % ("005930",'4','Y')

url = 'https://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd=005930&target=finsum_more'

dfs = pd.read_html(url)
df = dfs[0]
df = df.set_index('주요재무정보')
df.head()
df.head(10) # 10개 항목만 표시(실제 32개 항목)

##연습
from urllib.request import urlopen

url = "https://finance.naver.com/item/coinfo.nhn?code=005930&target=finsum_more"

result = urlopen(url)
result_html = result.read()
result_soup = BeautifulSoup(result_html, 'html.parser')
result_soup.find_all("a")

##https://wikidocs.net/80704 네이버 금융 사이트로부터 재무제표 데이터 파싱

import requests
import pandas as pd

def get_financial_statements(code):
    url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=%s&fin_typ=0&freq_typ=Y" % (code)
    html = requests.get(url).text

    html = html.replace('<th class="bg r01c02 endLine line-bottom"colspan="8">연간</th>', "")
    html = html.replace("<span class='span-sub'>(IFRS연결)</span>", "")
    html = html.replace("<span class='span-sub'>(IFRS별도)</span>", "")
    html = html.replace("<span class='span-sub'>(GAAP개별)</span>", "")
    html = html.replace('\t', '')
    html = html.replace('\n', '')
    html = html.replace('\r', '')

    for year in range(2009, 2021):
        for month in range(6, 13):
            month = "/%02d" % month
            html = html.replace(str(year) + month, str(year))

        for month in range(1, 6):
            month = "/%02d" % month
            html = html.replace(str(year+1) + month, str(year))

        html = html.replace(str(year) + '(E)', str(year))
    print("html : ", html)
    df_list = pd.read_html(html, index_col='주요재무정보')
    print('here')
    df = df_list[0]
    return df

if __name__ == "__main__":
    df = get_financial_statements('035720')
    print(df)

df = get_financial_statements('035720')



###### Dart api 사용
#https://medium.com/@doyourquant/dart-%EC%98%A4%ED%94%88-api%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-%EC%9E%AC%EB%AC%B4%EC%A0%9C%ED%91%9C-%ED%81%AC%EB%A1%A4%EB%A7%81-with-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%B9%84%EC%A0%95%EA%B7%9C%EC%A0%81%EC%9D%B8-%EC%BD%94%EB%94%A9-24f4acc7cdbe
#https://tariat.tistory.com/995
#기업개황자료 dart.company('005930')
#배당: dart.report('005930','배당',2018)
#재부재표: dart.finstate('삼성전자',2018)
#여러종목 재무제표 확인 dart.finstate('00126380,00164779, 00164742',2018)
#적절한 교육자료 https://nbviewer.jupyter.org/github/FinanceData/OpenDartReader/blob/master/docs/OpenDartReader_users_guide.ipynb?fbclid=IwAR2otfz5I-x-oz7CWIy9NBQh1HlrygF8VbqeKGHFvB4jFMp7pDHtHReWnUY
#다트 깃허브 자료실: https://github.com/FinanceData/OpenDartReader
#유용한 예시: https://nbviewer.jupyter.org/github/FinanceData/OpenDartReader/blob/master/docs/OpenDartReader_users_guide.ipynb
import dart_fss as dart
import OpenDartReader as op
import pandas as pd
상장주식정보 = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0] # 상장주식 정보
종목코드 = 상장주식정보['종목코드'].astype(str)

for i, item in enumerate(종목코드):
    if len(item)==4:
        종목코드[i] = "00"+item
    elif len(item)==5:
        종목코드[i] = "0"+item
    elif len(item)==3:
        종목코드[i] = "000"+item
    elif len(item)==2:
        종목코드[i] = "0000" + item
    elif len(item) == 1:
        종목코드[i] = "00000" + item

stock_list = ', '.join(종목코드)

api_key = 'e5428ec5e91df8e56250457aa6c0b04f08b58e4b'
dart = op(api_key)

fin = dart.finstate('삼성전자',2020)#reprt_code='11013') #'11013'은 1분기, 11012 2분기(반기) 11014 (3분기) 11011 사업보고서(4분기겠지?)
fin = dart.finstate('005280', 2020)
fin = dart.finstate(stock_list, 2020) # 검색이 되지 않는 항목은 리스트에서 제외한 후
# 에 다시 검색하는 방안으로?

fin.to_excel('210811 재무재표연습_total.xlsx',"w")
fin['thstrm_amount'] = pd.to_numeric(fin['thstrm_amount'].str.replace(',','')) # 한 열 숫자로 변환
fin = fin[fin['fs_nm']=='연결재무제표']
fin_pivot = fin.pivot_table(index=['stock_code','bsns_year'],columns=['fs_nm','account_nm'], values = 'thstrm_amount',aggfunc='mean')
fin_pivot.to_excel('210811 재무재표연습_total_pivot.xlsx',"w")




samsung = dart.report('005930','배당',2020)
#삼성전자 상장 이후 모든 공시 목록
sam_gongsea = dart.list('005930',start='1900')
sam_gongsea.to_excel('삼성전자 공시 목록.xlsx',"w")

#보고서 개별 문서를 부르기?
dart.retrieve(xls_url, '삼성전자_2018.xls')
dart.list_date_ex('2020-01-03')
rcp_no = '20190401004781'
dart.sub_docs(rcp_no)[:10]
dart.attach_doc_list(rcp_no)
attaches = dart.attach_file_list(rcp_no)
xls_url = attaches.loc[attaches['type']=='excel', 'url'].values[0]
dart.retrieve(xls_url, '삼성전자_2018.xls')