import requests

def _real(*, prod_code=None, fields=None, **data):
    url = 'https://api-ddc.wallstcn.com/market/real'
    data['prod_code'] = prod_code
    data['fields'] = fields
    r = requests.get(url, params=data)
    return r.json()

def gzsyl():
    """世界主要国债收益率
    """
    r = _real(
            prod_code='CN10YR.OTC,US10YR.OTC',
            fields='symbol,prod_code,prod_name,prod_en_name,preclose_px,price_precision,open_px,high_px,low_px,week_52_high,week_52_low,update_time,last_px,px_change,px_change_rate,market_type,trade_status'
    )
    for k,v in r['data']['snapshot'].items():
        print(*v)