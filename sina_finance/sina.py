import time
import requests

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
    url = 'https://hq.sinajs.cn/?_='+ str(int(round(time.time() * 1000))) + \
       '/&list=' + hf_code
    r = requests.get(url, headers=headers)
    print(r.text)

if __name__ == '__main__':
    go('hf_CL,hf_OIL,hf_XAU')
