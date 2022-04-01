import requests

headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/56.0.2924.87 Safari/537.36',
    }

EXCHANGE_TYPES = {
    '上交所': 0,
    '深交所': 1
}

def historical_prices(code, start, end, fields='TCLOSE;LCLOSE;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'):
    url = 'http://quotes.money.163.com/service/chddata.html'
    data = {
        'code': str(code),
        'start': str(start),
        'end': str(end),
        'fields': str(fields),
    }
    r = requests.post(url, data=data, headers=headers)
    r.encoding='gb2312'
    return r.text  

def zycwzb(code):
    url = 'http://quotes.money.163.com/service/zycwzb_' + str(code) + '.html'
    data = {
        'type': 'report'
    }
    r = requests.post(url, data=data, headers=headers)
    return r.text
