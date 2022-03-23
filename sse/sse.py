import pandas as pd
import requests
import time
import math
import random
import io
import json
import re
import sys

headers = {'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/56.0.2924.87 Safari/537.36',
           'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
           }

STOCK_TYPES = {
    1: '主板A股',
    2: '主板B股',
    8: '科创板'
}

DIVIDEND_FIELDS = {
    'SECURITY_CODE_A': 'A股股票代码',
    'RECORD_DATE_A': 'A股股权登记日',
    'EX_DIVIDEND_DATE_A': '除息日',
    'DIVIDEND_PER_SHARE1_A': '税后每股红利',
    'DIVIDEND_PER_SHARE2_A': '税前每股红利',
    'EXCHANGE_RATE': '-',
    'COMPANY_CODE': '公司代码',
    'FULL_NAME': '公司名称',
    'DIVIDEND_DATE': '股息日',
    'SECURITY_ABBR_A': '股票简称'
}

BONU_FIELDS = {
    'ANNOUNCE_DATE': '公告刊登日',
    'ANNOUNCE_DESTINATION': '公告宣布地',
    'BONUS_RATE': '送股比例',
    'CHANGE_RATE': '变动比例',
    'COMPANY_CODE': '股票代码',
    'COMPANY_NAME': '公司名称',
    'EX_RIGHT_DATE_A': '除权基准日',
    'EX_RIGHT_DATE_B': '除权基准日B',
    'LAST_TRADE_DATE_B': '最后交易日B',
    'RECORD_DATE_A': 'A股股权登记日',
    'RECORD_DATE_B': 'B股股权登记日',
    'SECURITY_CODE_A': 'A股证券代码',
    'SECURITY_CODE_B': 'B股证券代码',
    'SECURITY_NAME_A': 'A股证券名称',
    'SECURITY_NAME_B': 'B股证券名称',
    'TRADE_DATE_A': '红股上市日',
    'TRADE_DATE_B': 'B股红股上市日',
}

ALLOTMENTS_FIELDS = {
    'COMPANY_CODE': '公司代码',
    'END_DATE_OF_REMITTANCE_A': '配股缴款截止日',
    'EX_RIGHTS_DATE_A': 'A股除权交易日',
    'LISTING_DATE_A': '配股上市日',
    'PRICE_OF_RIGHTS_ISSUE_A': 'A股配股价格',
    'RATIO_OF_RIGHTS_ISSUE_A': '配股比例(10：?)',
    'RECORD_DATE_A': 'A股股权登记日',
    'SECURITY_CODE_A': 'A股证券代码',
    'SECURITY_NAME_A': '证券名称',
    'START_DATE_OF_REMITTANCE_A': '配股缴款起始日',
    'TRUE_COLUME_A': '实际配股量(万股)',
}


def __regular_stocks(df):
    del(df['Unnamed: 5'])
    del(df['公司代码 '])
    del(df['公司简称 '])
    df['交易所'] = 0
    df['所属行业'] = ''
    df['代码'] = df['代码'].astype(str)
    return df


def call_download_stock_list_file(stock_type):
    headers = {'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/56.0.2924.87 Safari/537.36',
               'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
               }
    url = 'http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName='
    data = {
        'stockType': stock_type
    }
    r = requests.post(url, data=data, headers=headers)
    print(r.text)
    df = pd.read_table(io.StringIO(r.text))
    return pd.read_table(io.StringIO(r.text))

def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')

def common_query(**data):
    url='http://query.sse.com.cn/commonQuery.do'
    data['jsonCallBack'] = 'jsonpCallback' + \
        str(math.floor(1e5 * random.random()))
    data['_'] = str(int(round(time.time() * 1000)))
    r=requests.get(url, params=data, headers=headers)
    return loads_jsonp(r.text)

def security_list(**data):
    url='http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName='
    r=requests.get(url,params=data,headers=headers)
    return r.text

# 得到分红
def get_dividends(year):
    data = {
        'isPagination': 'false',
        'sqlId': 'COMMON_SSE_GP_SJTJ_FHSG_AGFH_L_NEW',
        'record_date_a': year,
        'security_code_a': '',
    }
    result = call_common_query(data)
    return result['result']
    # return pd.DataFrame(result['result'])

# 得到送股
def get_bonus(year):
    data = {
        'isPagination': 'false',
        'sqlId': '',
        'year1': year,
        'year2': year,
    }
    result = call_common_query(data)
    return pd.DataFrame(result['result'])

# 得到配股
def get_allotments(year):
    data = {
        'isPagination': 'false',
        'sqlId': 'COMMON_SSE_GP_SJTJ_MJZJ_PG_AGPG_L',
        'searchyear': year,
    }
    result = call_common_query(data)
    return pd.DataFrame(result['result'])

def overview(SEARCH_DATE='', PRODUCT_CODE='01,02,03,11,17'):
    r=common_query(
        sqlId='COMMON_SSE_SJ_GPSJ_CJGK_MRGK_C',
        isPagination='false',
        PRODUCT_CODE=PRODUCT_CODE,
        type='inParams',
        SEARCH_DATE=SEARCH_DATE
        )
    for i in r['result']:
        print(i['PRODUCT_CODE'], i['TRADE_DATE'], i['LIST_NUM'], i['TOTAL_VALUE'], \
            i['NEGO_VALUE'], i['TRADE_AMT'], i['TRADE_VOL'], i['AVG_PE_RATE'], \
                i['TOTAL_TO_RATE'], i['NEGO_TO_RATE'])

if __name__ == '__main__':
    # 得到分红
    # print(common_query(sqlId='COMMON_SSE_GP_SJTJ_FHSG_AGFH_L_NEW', record_date_a=2021, security_code_a='', isPagination='false'))
    # 得到送股
    # print(common_query(sqlId='COMMON_SSE_GP_SJTJ_FHSG_SG_L_NEW', isPagination='false', year1=2021, year2=2021))
    # overview(sys.argv[1], sys.argv[2])
    # call_download_stock_list_file(1)
    print(security_list(stockType=1))