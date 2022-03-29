import time
import requests
import json

headers = {
    # ':authority': 'www.chinamoney.com.cn',
    # ':method': 'POST',
    # ':path': '/r/cms/www/chinamoney/data/currency/bk-lpr.json?t=1648084105901',
    # ':scheme': 'https',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-length': '0',
    'cookie': 'apache=4a63b086221745dd13be58c2f7de0338; lss=df66127dd86a035c29bb9af442648995; _ulta_id.CM-Prod.e9dc=646f66c46fe051af; _ulta_ses.CM-Prod.e9dc=de49b9ab678337fb; AlteonP10=BHoVdiw/F6yOwcFLkPTcRA$$',
    'origin': 'https://www.chinamoney.com.cn',
    'referer': 'https://www.chinamoney.com.cn/chinese/bklpr/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Microsoft Edge";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46',
    'x-requested-with': 'XMLHttpRequest',
}

def _chinamoney(**data):
    url = 'https://www.chinamoney.com.cn/r/cms/www/chinamoney/data/currency/bk-lpr.json'
    data['t'] = str(int(round(time.time() * 1000)))
    r = requests.post(url, data=data, headers=headers)
    return json.loads(r.text)

def lpr():
    r = _chinamoney()
    print(r['data']['showDateCN'], r['records'][0]['termCode'], r['records'][0]['shibor'])
    print(r['data']['showDateCN'], r['records'][1]['termCode'], r['records'][1]['shibor'])

if __name__ == '__main__':
    lpr()
