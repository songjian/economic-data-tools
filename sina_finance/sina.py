import time
import requests
from bs4 import BeautifulSoup
import io
import pandas as pd

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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71',
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

def cwzy(code):
    """财务摘要
    写这个方法主要是为了拿到每股净资产，写到一般发现有更好的方法或者这个数据。新的方法是 mgjzc
    """
    url='https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/'+code+'.phtml'
    r=requests.get(url)
    soup=BeautifulSoup(r.text, 'html.parser')
    return soup.find('table', id='FundHoldSharesTable').find_all('td', class_='tdr')

def mgjzc(code):
    """每股净资产
    """
    url='https://vip.stock.finance.sina.com.cn/corp/view/vFD_FinanceSummaryHistory.php?stockid='+code+'&type=mgjzc'
    r=requests.get(url)
    soup=BeautifulSoup(r.text, 'html.parser')
    csv_buffer=io.StringIO()
    for tr in soup.find('table', id='Table1').tbody.find_all('tr'):
        td = tr.find_all('td')
        csv_buffer.write(td[0].get_text()+','+td[1].get_text()+"\n")
    csv_buffer.seek(0)
    return pd.read_csv(csv_buffer)