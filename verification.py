import openpyxl
from bs4 import BeautifulSoup
import requests
import time
import random

class test():
    def __init__(self):
        self.URL = 'http://dart.fss.or.kr/corp/searchCorp.ax'

    def read_xlsx(self):
        wb = openpyxl.load_workbook('종목리스트_통합_19.08.18.xlsx')
        ws = wb.active
        result = []
        for r in ws.rows :
            result.append(r[2].value.strip())
        return result

    def rand_float(self):
        return random.random()

    def write_down(self, comp_name):
        with open('not_in_list.txt', 'at') as f :
            f.write(comp_name)
            f.write("\n")

    def main(self):
        idx = 0
        comp_name_li = self.read_xlsx()

        # data = {'textCrpNm' : 'ㅇㅇ'}
        # req = requests.post(self.URL, data)
        # soup = BeautifulSoup(req.content, 'html.parser')
        # result = soup.select_one('.table_scroll table tr .end.no_data2')
        #
        # if result == None :
        #     print(idx)
        #     idx += 1
        # else :
        #     print("ㅇㅇ")
        #     self.write_down("ㅇㅇ")

        for comp_name in comp_name_li :
            data = {'textCrpNm' : comp_name}
            req = requests.post(self.URL, data)
            soup = BeautifulSoup(req.content, 'html.parser')
            result = soup.select('.table_scroll table tr .end.no_data2')
            if result :
                print(comp_name)
                self.write_down(comp_name)
            else :
                print(idx)
                idx += 1

            time.sleep(self.rand_float())

if __name__ == "__main__" :
    test().main()