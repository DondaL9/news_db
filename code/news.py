from WindPy import w
w.start()
print(w.isconnected())


#test retriving news data and save it in a database
#get hs300 consituent stocks
stk_lst = w.wset("sectorconstituent","date=2020-11-21;windcode=000300.SH").Data[1]
news_1 = w.wnd("000001.SZ", "2020-11-01 00:00:00", "2020-11-21 16:17:00")













w.stop()
