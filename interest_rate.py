import numpy as np
import pandas as pd
import requests

__all__ = ['update_interest_rate']

FILE_PATH = '~/quant/jupyter-data-dir/金融/抓取股票数据/data/ccb/interest_rate.csv'

DATES = {
    '2015-10-24': '20151024_1445618390',
    '2015-08-26': '20150825_1440515878', 
    '2015-06-28': '20150627_1435415352', 
    '2015-05-11': '20150510_1431269889', 
    '2015-02-28': '20150228_1425136078', 
    '2014-11-22': '20141121_1416584180', 
    '2012-07-06': '20120705_1341503961', 
    '2012-06-08': '20120607_1339072330', 
    '2011-07-07': '20110706_1309964418', 
    '2011-04-06': '20110405_1302013313', 
    '2011-02-09': '20110208_1297169241', 
    '2010-12-26': '20101225_1293282539', 
    '2010-10-20': '20101019_1287499850', 
    '2008-12-23': '20090729_1248853092', 
    '2008-11-27': '20090729_1248854223', 
    '2008-10-30': '20090730_1248918018', 
    '2008-10-09': '20090730_1248918369', 
    '2007-12-21': '20090730_1248918607', 
    '2007-09-15': '20090730_1248918785', 
    '2007-08-22': '20090730_1248918943', 
    '2007-07-21': '20090730_1248919091', 
    '2007-05-19': '20090730_1248919248', 
    '2007-03-18': '20090730_1248919402', 
    '2006-08-19': '20090730_1248919957', 
    '2004-10-29': '20090730_1248920350', 
    '2002-02-21': '20090730_1248920493', 
    '1999-06-10': '20090730_1248920621', 
    '1998-12-07': '20090730_1248920735', 
    '1998-07-01': '20090730_1248920866', 
    '1998-03-25': '20090730_1248920987', 
    '1997-10-23': '20090730_1248921233', 
    '1996-08-23': '20090730_1248921362', 
    '1996-05-01': '20090730_1248921482', 
#     '1955-10-01': '20090730_1248921591', 
}

def __get_ccb_interest_rate(fdate):
    url = 'http://www.ccb.com/cn/personal/interestv3/' + fdate + '.html'
    data = {}
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/56.0.2924.87 Safari/537.36',
        'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
    }
    r = requests.get(url, data=data, headers=headers)
#    return r.text
    df = pd.read_html(r.text)[0]
    df = df.iloc[5:11]
    df.set_index(0, inplace=True)
    return df[1]
    """
def update_interest_rate():
    df = pd.DataFrame()
    for date,fdate in DATES.items():
        df[date] = get_ccb_interest_rate(fdate)
    df.T.to_csv(FILE_PATH)
    
def __interest_rate():
    return pd.read_csv(FILE_PATH, index_col=0, parse_dates=[0]).sort_index()

def three_month():
    return __interest_rate()['三个月']
"""
if __name__ == '__main__':
    print(__get_ccb_interest_rate('20090730_1248921482'))
#     update_interest_rate()
