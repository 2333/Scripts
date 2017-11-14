# encodeing="utf-8"
import urllib
import urllib.request
from bs4 import BeautifulSoup

url = "http://data.eastmoney.com/xg/xg/default.html"
# url = "http://stock.stockstar.com/ipo/ipo_8_1_1.htm"

req = urllib.request.urlopen(url).read()
print(type(req))
data = req
soup = BeautifulSoup(req.decode("utf-8", 'ignore'))
print(soup)
