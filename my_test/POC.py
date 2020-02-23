# 12초에 한번

from bs4 import BeautifulSoup
import requests

class POC():
    def __init__(self):
        self.URL = 'http://dart.fss.or.kr/dsab001/search.ax'
        self.header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                       'Referer' : 'http://dart.fss.or.kr/'}
        self.search_info = {'currentPage' : '1',
                            'maxResults' : '100',
                            'maxLinks' : '10',
                            'sort' : 'date',
                            'series' : 'desc',
                            'textCrpNm' : '삼성전자',
                            'finalReport' : 'recent',
                            'startDate' : '20190423',
                            'endDate' : '20191023',
                            'publicType' : ['A001', 'A002', 'A003', 'A004', 'A005']
                            }

    def get_data(self):
        data = {**self.search_info, **self.header}
        req = requests.post(self.URL, data)
        soup = BeautifulSoup(req.content, 'html.parser')
        # print(soup.prettify())
        table = soup.select('tbody tr')
        for row in table :
            href = row.select('td')[2].select_one('a')['href']
            print('http://dart.fss.or.kr' + href)

if __name__ == "__main__" :
    POC().get_data()