from bs4 import BeautifulSoup
import requests


class Cur_data:
    def __init__(self):
        self.URL = "http://dart.fss.or.kr/dsac001/mainAll.do"
        req = requests.get(self.URL)
        soup = BeautifulSoup(req.content, "html.parser")
        self.rows = soup.select(".table_list > table > tr")

    def my_trim(self, word):
        word = word.strip().replace("\r", "").replace("\n", "").replace("\t", "")
        # print(word)
        return word

    def get_cur_data(self, idx):
        raw_cur_comp = self.rows[idx].select_one(".nobr1").text
        cur_comp = self.my_trim(raw_cur_comp)
        # print(cur_comp)

        raw_cur_report = self.rows[idx].select("td")[2].text
        cur_report = self.my_trim(raw_cur_report)
        # print(cur_report)

        href = self.rows[idx].select("a")[1]["href"]
        # print(href)
        link = "".join(["http://dart.fss.or.kr", href])

        return cur_comp, cur_report, link
