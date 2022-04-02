import time
import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'hq.sinajs.cn',
    'Referer': 'https://finance.sina.com.cn/futures/quotes/CL.shtml',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Microsoft Edge";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52',
}

def go(hf_code):
    url = 'https://hq.sinajs.cn/?_=' + str(int(round(time.time() * 1000))) + \
        '/&list=' + hf_code
    r = requests.get(url, headers=headers)
    print(r.text)

def zcfzb(code, year='part'):
    """资产负债表
    """
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Cache-Control'] = 'max-age=0'
    headers['Host'] = 'vip.stock.finance.sina.com.cn'
    headers['If-Modified-Since'] = 'Thu, 31 Mar 2022 08:06:16 GMT'
    headers['Upgrade-Insecure-Requests'] = '1'
    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/' + \
        code+'/ctrl/'+year+'/displaytype/4.phtml'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    col_len = len(soup.tbody.tr.find_all('td'))
    for tr in soup.tbody.find_all('tr'):
        td = tr.find_all('td')
        if col_len == len(td):
            for t in td:
                print(t.text, end=' ')
            print()