import pandas as pd
import requests
import random
import re
import json

headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/56.0.2924.87 Safari/537.36',
        'Referer': 'http://www.szse.cn/market/product/stock/list/index.html',
    }

STOCK_FIELDS = {
    'bk': '板块',
    'agdm': '代码',
    'agjc': '简称',
    'agssrq': '上市日期',
    'sshymc': '所属行业',
}

def api(**data):
    url='http://www.szse.cn/api/report/ShowReport/data'
    data['SHOWTYPE']='JSON'
    data['CATALOGID']='1803_sczm'
    data['loading']='first'
    data['random']=str(random.random())
    r=requests.get(url,params=data,headers=headers)
    return json.loads(r.text)

def overview():
    r=api()
    for i in r[0]['data']:
        print(i['lbmc'], i['zqsl'], i['cjje'], i['cjsl'], i['sjzz'], i['ltsz'], i['zgb'], i['ltgb'])
    
    

def __regular_stocks(df):
    df['agjc'] = df.apply(lambda x: re.compile(r'<[^>]+>',re.S).sub('', x['agjc']), axis=1)
    return df

def get_szse_stocks():
    pageno = 1
    pagecount = 0
    df = pd.DataFrame()
    
    while (pageno != pagecount):
        url = 'http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1&PAGENO=' + str(pageno) + '&random=' + str(random.random())
        r = requests.get(url, headers=headers)
        pageno = r.json()[0]['metadata']['pageno'] + 1
        pagecount = r.json()[0]['metadata']['pagecount']
        df = df.append(pd.DataFrame(r.json()[0]['data']), ignore_index=True)
    return __regular_stocks(df)

if __name__ == '__main__':
    overview()