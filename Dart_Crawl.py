import openpyxl
from lib.Cur_data import Cur_data
from bs4 import BeautifulSoup
import requests
import sqlite3
from apscheduler.schedulers.blocking import BlockingScheduler

class Dart_Crawl() :
    def __init__(self):
        self.comp_list = self.read_xlsx()
        self.c = self.set_db()[1]

    def set_db(self):
        conn = sqlite3.connect('./data/data.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS data(comp text, report text, link text)")
        return conn, c

    def read_xlsx(self):
        wb = openpyxl.load_workbook('./res/종목리스트_통합_19.08.18.xlsx')
        ws = wb.active
        comp_list = []
        for r in ws.rows:
            comp_list.append(r[2].value)
        return comp_list

    def get_db(self):
        comp = self.c.execute('SELECT comp FROM data')
        comp = self.c.fetchall()[0][0]

        report = self.c.execute('SELECT report FROM data')
        report = self.c.fetchall()[0][0]

        link = self.c.execute('SELECT link FROM data')
        link = self.c.fetchall()[0][0]

        return comp, report, link

    def is_verified(self, comp_name):
        if comp_name in self.comp_list :
            return True

    def compare(self, db_link, cur_link):
        if db_link == cur_link :
            return True

    def append_result(self, result, comp_name, report, link):
        result.append({'comp_name': comp_name, 'report': report, 'link': link})

    def main(self):
        result = []
        idx = 0

        db = self.get_db()
        db_link = db[2]

        cd = Cur_data()
        while(idx < 100) :
            cur_data = cd.get_cur_data(idx)
            cur_comp = cur_data[0]
            cur_report = cur_data[1]
            cur_link = cur_data[2]
            if self.is_verified(cur_comp) :
                if not(self.compare(db_link, cur_link)) :
                    self.append_result(result, cur_comp, cur_report, cur_link)
                    idx += 1
                else :
                    return result
            else :
                idx += 1
        return result

if __name__ == "__main__" :
    result = Dart_Crawl().main()
    print(result)