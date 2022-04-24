import pandas as pd
import requests
code = '005930'
URL = f"https://finance.naver.com/item/main.nhn?code={code}"
r = requests.get(URL)
df = pd.read_html(r.text)[3]

URL = f"https://finance.naver.com/item/coinfo.naver?code={code}&target=finsum_more"
r = requests.get(URL)
slist = pd.read_html(r.text)
df = pd.read_html(r.text)[3]