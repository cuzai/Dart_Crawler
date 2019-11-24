import openpyxl
from bs4 import BeautifulSoup
import requests
import sqlite3
from apscheduler.schedulers.blocking import BlockingScheduler


class Dart_Crawl() :
    def __init__(self):
        self.URL = 'http://dart.fss.or.kr/dsac001/mainAll.do'
        self.conn = sqlite3.connect('./data.db', check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS data(comp text, report text)")

    def read_xlsx(self):
        wb = openpyxl.load_workbook('종목리스트_통합_19.08.18.xlsx')
        ws = wb.active
        result = []
        for r in ws.rows :
            result.append(r[2].value)
        return result

    def save_db(self, current_first_comp, current_first_report) :
        # self.c.execute('INSERT INTO data VALUES(?, ?)', (current_first_comp,current_first_report))
        self.c.execute('UPDATE data SET comp = ?', (current_first_comp, ))
        self.c.execute('UPDATE data SET report = ?', (current_first_report, ))
        self.conn.commit()

    def get_db(self):
        comp = self.c.execute('SELECT comp FROM data')
        comp = self.c.fetchall()[0][0]

        report = self.c.execute('SELECT report FROM data')
        report = self.c.fetchall()[0][0]

        return comp, report

    def compare(self, new_first_comp, new_first_report):
        if self.current_first_comp == new_first_comp and self.current_first_report == new_first_report:
            return True

    def my_trim(self, word):
        word = word.strip().replace("\r", "").replace("\n", "").replace("\t", "")
        # print(word)
        return word
    def crawl(self):
        current = self.get_db()
        self.current_first_comp = current[0]
        self.current_first_report = current[1]

        req = requests.get(self.URL)
        soup = BeautifulSoup(req.content, 'html.parser')

        first_row = soup.select_one('.table_list > table > tr')
        new_first_comp = first_row.select_one('.nobr1').text
        new_first_comp = self.my_trim(new_first_comp)
        # print(new_first_comp)
        new_first_report = first_row.select('td')[2].text
        new_first_report = self.my_trim(new_first_report)
        # print(new_first_report)

        # compare current and old
        if self.compare(new_first_comp, new_first_report) :
            print("already same")
            return
        else :
            # save current first
            self.save_db(new_first_comp, new_first_report)
            rows = soup.select('.table_list > table > tr')

            # get links
            result = []
            for row in rows :
                comp_name = row.select_one('.nobr1').text
                comp_name = self.my_trim(comp_name)
                # print(comp_name)

                report = row.select('td')[2].text
                report = self.my_trim(report)
                # print(report)

                href = row.select('a')[1]['href']
                # print(href)
                link = "".join(['http://dart.fss.or.kr/', href])
                # print(link)

                if comp_name == self.current_first_comp and report == self.current_first_report:
                    print(result)
                    return
                else :
                    result.append({'comp_name' : comp_name, 'report' : report, 'link' : link})

if __name__ == "__main__" :
    # Dart_Crawl().my_trim("기타시장안내\r\n\t\t\t\t\t\t\t\r\n  \t\t\t\t\t\t\t(관리종목 지정우려 예고)")
    # Dart_Crawl().crawl()
    sched = BlockingScheduler()
    sched.add_job(Dart_Crawl().crawl, 'cron', second='*/5')
    sched.start()