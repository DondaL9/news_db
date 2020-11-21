from typing import Any, Union, Tuple

from WindPy import w
import sqlite3
import csv
from pandas import DataFrame
w.start()
print(w.isconnected())

conn = sqlite3.connect('../data/news.db')
cur = conn.cursor()
#test retriving news data and save it in a database
#get hs300 consituent stocks
stk_lst = w.wset("sectorconstituent","date=2020-11-21;windcode=000300.SH").Data[1]
start_date = "2020-01-01 00:00:00"
end_date = "2020-11-21 15:00:00"

cur.execute('''DROP TABLE IF EXISTS news''')
cur.execute('''
CREATE TABLE IF NOT EXISTS news
('id','title','time','url','source','abstract','relevant_windcodes','important')
''')
error_stk_lst = []
for stk in stk_lst:
    print(stk)
    news_stk = w.wnd(stk, start_date, end_date)
    # news_stk = w.wnd("000001.SZ", start_date, end_date)
    # rearrange the data
    if news_stk.ErrorCode != 0:
        error_stk_lst.append(stk)
        pass
    else:
        info = []
        for i in range(len(news_stk.Data[0])):
            temp = []
            for j in range(len(news_stk.Fields)):
                temp.append(news_stk.Data[j][i])
            info.append(tuple(temp))
        cur.executemany("""
            Insert Into news 
            VALUES (?,?,?,?,?,?,?,?)
            """, info)
# Save (commit) the changes
conn.commit()
# close the connection
conn.close()

with open('../data/error_code.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(error_stk_lst)








w.stop()
