import numpy as np
import pandas as pd
import requests
import random
from sqlalchemy import create_engine
import io
import re

SQLITE_PATH = '/home/sj/workspace/workspace_python/金融/抓取股票数据/stock.sqlite'

engine = create_engine('sqlite:///' + SQLITE_PATH)
conn = engine.connect()

STOCK_FIELDS = {
    'bk': '板块',
    'agdm': '代码',
    'agjc': '简称',
    'agssrq': '上市日期',
    'sshymc': '所属行业',
}

def __regular_stocks(df):
    df['agjc'] = df.apply(lambda x: re.compile(r'<[^>]+>',re.S).sub('', x['agjc']), axis=1)
    return df

def get_szse_stocks():
    pageno = 1
    pagecount = 0
    df = pd.DataFrame()
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/56.0.2924.87 Safari/537.36',
        'Referer': 'http://www.szse.cn/market/product/stock/list/index.html',
    }
    while (pageno != pagecount):
        url = 'http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1&PAGENO=' + str(pageno) + '&random=' + str(random.random())
        r = requests.get(url, headers=headers)
        pageno = r.json()[0]['metadata']['pageno'] + 1
        pagecount = r.json()[0]['metadata']['pagecount']
        df = df.append(pd.DataFrame(r.json()[0]['data']), ignore_index=True)
    return __regular_stocks(df)

def update_stocks():
    df = get_szse_stocks()[['bk', 'agdm', 'agjc', 'agssrq', 'sshymc']].rename(columns=STOCK_FIELDS)
    df['交易所'] = 1
    df.to_sql('stock_list', engine, chunksize=1000, if_exists='append', index=False)