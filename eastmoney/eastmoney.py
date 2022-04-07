import time
import math
import random
import json
import re
import requests

headers={
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'datainterface.eastmoney.com',
    'Referer': 'https://data.eastmoney.com/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29',
}

def _loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?\((.*)\).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')

def _js(**data):
    url='https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx'
    data['cb']='jQuery' + \
        str(math.floor(1e10 * random.random())) + \
        '_' + str(int(round(time.time() * 1000)))
    data['_'] = str(int(round(time.time() * 1000)))
    data['type'] = 'GJZB'
    data['js'] = '([(x)])'
    data['p'] = '1'
    data['ps'] = '200'
    r = requests.get(url, params=data, headers=headers)
    return _loads_jsonp(r.text)

def hg(*, stat=None, mkt=None, sty='HKZB'):
    """宏观数据
    """
    data=_js(stat=stat, mkt=mkt, sty=sty)
    for i in data:
        print(i)