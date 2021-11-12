#https://gomjellie.github.io/%ED%8C%8C%EC%9D%B4%EC%8D%AC/pandas/%EC%A3%BC%EC%8B%9D/2017/06/09/pandas-datareader-stock.html
#from pandas_datareader import data as pdr  #여기서 오류 났었으나, fred.py란 파일을 수정하여 해결

from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
yf.pdr_override()
start_date = '2018-01-06'
end_date = '2018-10-02'
tickers = ['017800.KS','047440.KQ','238090.KQ']  #코스닥엔 KQ, 코스피에 KS가 붙음
tic0 = pdr.get_data_yahoo(tickers[0],start_date)
tic1 = pdr.get_data_yahoo(tickers[1],start_date, end_date)
tic2 = pdr.get_data_yahoo(tickers[2],start_date, end_date)

import pandas_datareader.data as web
import datetime
amzn = web.DataReader("AMZN","yahoo",'2010-01-01',"2011-01-01")