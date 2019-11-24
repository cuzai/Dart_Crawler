import sqlite3

conn = sqlite3.connect('./data.db')
c = conn.cursor()

c.execute("UPDATE data SET comp = ? ", ("씨씨에스", ))
c.execute("UPDATE data SET report = ? ", ("최대주주변경", ))
conn.commit()

conn.close()
