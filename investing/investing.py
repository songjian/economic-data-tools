import requests
import pandas as pd
import datetime
import time


class Investing:
    base_url = 'https://cn.investing.com/instruments/HistoricalDataAjax'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
               'X-Requested-With': 'XMLHttpRequest'
               }
    
    def historical_data(self, curr_id, st_date, end_date):
        """获得历史数据

        Parameters:
        curr_id(str):Investing.com网站自己的品种编号
        st_date(str):开始时间，格式:2019/09/01
        end_date(str):结束时间，格式:2019/09/01

        Returns
        pandas.Series
        """
        data={
            'curr_id': curr_id,
            'smlID': '204958',
            'header': '',
            'st_date': st_date,
            'end_date': end_date,
            'interval_sec': 'Daily',
            'sort_col': 'date',
            'sort_ord': 'DESC',
            'action': 'historical_data'
        }
        r=requests.post(self.base_url, data=data, headers=self.headers)
        return r.text


    def _get_data(self, stock_list, st_date):
        # st_date = '2019/09/01'
        end_date = time.strftime('%Y/%m/%d', time.localtime())
        dfs = pd.DataFrame()
        for stock, curr_id in stock_list.items():
            data = {
                'curr_id': curr_id,
                'smlID': '204958',
                'header': '',
                'st_date': st_date,
                'end_date': end_date,
                'interval_sec': 'Daily',
                'sort_col': 'date',
                'sort_ord': 'DESC',
                'action': 'historical_data'
            }

            r = requests.post(self.base_url, data=data, headers=self.headers)
            tables = pd.read_html(r.text)
            tables[0]
            dfs[stock] = pd.Series(list(tables[0]['收盘']), index=list(
                tables[0]['日期'].apply(lambda x: datetime.strptime(x, "%Y年%m月%d日"))))
        dfs.sort_index(axis=0, inplace=True, ascending=True)
        return dfs
