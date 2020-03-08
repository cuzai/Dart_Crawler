import openpyxl
from lib.Cur_data2 import Cur_data
import sqlite3
from apscheduler.schedulers.background import BlockingScheduler
import requests
import simplejson as json
import time


class Dart_Crawl:
    def __init__(self):
        self.comp_list = self.read_xlsx()
        db = self.set_db()
        self.conn = db[0]
        self.c = db[1]

    def set_db(self):
        conn = sqlite3.connect("./data/data.db", check_same_thread=False)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS data(comp text, report text, link text)")
        return conn, c

    def read_xlsx(self):
        wb = openpyxl.load_workbook("./res/종목리스트_통합_19.08.18.xlsx")
        ws = wb.active
        comp_list = []
        for r in ws.rows:
            comp_list.append(r[2].value)
        return comp_list

    def save_db(self, cur_first_comp, cur_first_report, cur_first_link):
        self.c.execute("UPDATE data SET comp = ?", (cur_first_comp,))
        self.c.execute("UPDATE data SET report = ?", (cur_first_report,))
        self.c.execute("UPDATE data SET link = ?", (cur_first_link,))
        self.conn.commit()

    def get_db(self):
        comp = self.c.execute("SELECT comp FROM data")
        comp = self.c.fetchall()[0][0]

        report = self.c.execute("SELECT report FROM data")
        report = self.c.fetchall()[0][0]

        link = self.c.execute("SELECT link FROM data")
        link = self.c.fetchall()[0][0]

        return comp, report, link

    def is_verified(self, comp_name):
        if comp_name in self.comp_list:
            return True

    def is_same(self, db_link, cur_link):
        if db_link == cur_link:
            return True

    def append_result(self, result, comp_name, report, link):
        result["data"].append(
            {"company_name": comp_name, "report": report, "link": link}
        )

    def main(self):
        result = {"data": []}
        idx = 1
        is_first = True

        db = self.get_db()
        db_link = db[2]

        cd = Cur_data()
        while idx < 100:
            try:
                cur_data = cd.get_cur_data(idx)
            except IndexError:
                pass
            cur_comp = cur_data[0]
            cur_report = cur_data[1]
            cur_link = cur_data[2]
            if self.is_verified(cur_comp):
                if not (self.is_same(db_link, cur_link)):
                    if is_first:
                        self.save_db(cur_comp, cur_report, cur_link)
                        is_first = False
                    self.append_result(result, cur_comp, cur_report, cur_link)
                    # print(json_idx, cur_comp, cur_report, cur_link)
                else:
                    print(result)
                    return

            idx += 1

        response = requests.post(
            url="https://investalk.vingokorea.com/data",
            # url="http://127.0.0.1:8080/test",
            data=json.dumps(result),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        print("post")
        print("status_code : ", response.status_code)
        print(response.json)
        print(result)
        with open("test.txt", "a") as a:
            a.write(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    # Dart_Crawl().main()
    sched = BlockingScheduler()
    sched.add_job(
        # Dart_Crawl().main,
        # "cron",
        # second="*/4",
        # hour="7-18",
        # day_of_week="mon-fri"
        Dart_Crawl().main,
        "cron",
        second="*/4",
        # hour="7-22",
    )
    sched.add_job(Dart_Crawl().main, "cron", hour="22", day_of_week="mon-fri")

    sched.start()
