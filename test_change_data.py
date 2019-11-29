import sqlite3

conn = sqlite3.connect('./data/data.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS data(comp text, report text, link text)")
c.execute("INSERT INTO data VALUES(?, ?, ?) ", ("흥아해운", "[기재정정]타법인주식및출자증권처분결정", "http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20191129800730"))
conn.commit()

conn.close()
