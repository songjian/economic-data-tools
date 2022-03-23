#!/usr/bin/env python3

import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from datetime import datetime
import matplotlib.pyplot as plt
import requests
import requests_cache
import time
import math
from sqlalchemy import create_engine
import execjs
import random
import io
import json
import os

TMP_PATH = '/home/sj/workspace/workspace_python/金融/tmp/'
SQLITE_PATH = '/home/sj/workspace/workspace_python/金融/抓取股票数据/stock.sqlite'

engine 
__create_engine('sqlite:///' + SQLITE_PATH)

EXCHANGE_TYPES = {
    '上交所': 0,
    '深交所': 1
}

def __create_engine(url):
    globla engine
    engine = create_engine(url)

def __filepath(filename):
    return TMP_PATH + str(filename) + '.csv'

def __tmpdir():
    return TMP_PATH

def update_prices(start, end):
    allstocks = pd.read_sql_table('stock_list', engine.connect())
    allstocks.apply(lambda x: download_historical_prices(x['代码'], x['交易所'], start, end), axis=1)
    
    error_stocks = []
    for root, dirs, files in os.walk(__tmpdir(), topdown=False):
        for file in files:
            filepath = root + file
            try :
                df = pd.read_csv(filepath)
                regular(df).to_sql('historical_prices', engine, index=False, if_exists='append')
            except :
                error_stocks.append(file)
    return error_stocks

def download_historical_prices(code, exchange, start, end, fields=None):
    fields = 'TCLOSE;LCLOSE;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP' if fields == None else fields
    url = 'http://quotes.money.163.com/service/chddata.html'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/56.0.2924.87 Safari/537.36',
    }
    data = {
        'code': str(exchange) + str(code),
        'start': start,
        'end': end,
        'fields': fields,
    }
    r = requests.post(url, data=data, headers=headers)
    r.encoding='gb2312'
    with open(__filepath(code), 'w', encoding='utf-8') as f:
        f.write(r.text)
        
def update_today_prices():
    today = datetime.now().strftime('%Y%m%d')
    update_prices(today, today)

def get_netease_zycwzb(code):
    url = 'http://quotes.money.163.com/service/zycwzb_' + str(code) + '.html'
    data = {
        'type': 'report'
    }
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/56.0.2924.87 Safari/537.36',
        'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
    }
    r = requests.post(url, data=data, headers=headers)
    return pd.read_csv(io.StringIO(r.text), index_col=0)

def update_historical_data_from_netease(end=None):
    if(end == None):
        end = datetime.now().strftime('%Y%m%d')
    stocks = pd.read_sql_table('stock_list', engine.connect(), index_col='index')
    stocks.apply(lambda row: get_netease_historical_data(EXCHANGE_TYPES[row['交易所']], row['代码'], end=end), axis=1)

def regular(df):
    df.sort_index(inplace=True)
    df['股票代码'] = df['股票代码'].apply(lambda x: x.lstrip("'"))
    df['收盘价'].replace(0, np.NaN, inplace=True)
    df['收盘价'].fillna(method='ffill' , inplace=True)
    df.dropna(inplace=True)
    return df

def restoration_of_rights(df):
    df['收益率'] = df['收盘价'] / df['前收盘'] - 1
    df.iloc[0,-1] = np.NaN
    df['后复权'] = df.iloc[0]['收盘价'] * (1 + df.loc[:,'收益率']).cumprod()
    return df