import sqlite3

conn = sqlite3.connect('./data/data.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS data(comp text, report text, link text)")
c.execute("INSERT INTO data VALUES(?, ?, ?) ", ("포티스", "[기재정정]주주총회소집결의", "http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20191129900581"))
conn.commit()

conn.close()
