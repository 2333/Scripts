# encodeing="utf-8"
import urllib
import urllib.request
from bs4 import BeautifulSoup
import json
from datetime import *

url = "http://data.eastmoney.com/xg/xg/default.html"
# url = "http://stock.stockstar.com/ipo/ipo_8_1_1.htm"
# 这个连接可以拿到json数据
dataurl = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=XGSG_LB&token=70f12f2f4f091e459a279469fe49eca5&st=purchasedate,securitycode&sr=-1&p=1&ps=50&js=(x)&rt=50352348"
# 拿到新股json数据加载成json
stock = urllib.request.urlopen(dataurl).read()
datajson = json.loads(stock.decode("utf-8"))
assert datajson is not ""

# 检索今天的新股
#  use +timedelta(days=1) to set days
time = (date.today()+timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
mes = str(date.today()+timedelta(days=1)) + " 新股信息\n"
for i in datajson:
    # print(i.get("purchasedate"), i.get("securityshortname"), time)
    if i.get("purchasedate") == time:
        price = i.get("issueprice") if isinstance(i.get("issueprice"),float) else "(预估)" + str(i.get("jg1"))
        mes += """
新股名称：%s
申购代码：%s
发行价格：%s元/股
申购上限：%s股
参考行业：%s
""" % (i.get("securityshortname"), i.get("subcode"),
        price , int(i.get("applyont")), i.get("INDUSTRY"))
        lwrandate = i.get("lwrandate")

try:
    sh_emoji = chr(0x1f389)
    lwrandate = datetime.strptime(lwrandate, "%Y-%m-%dT%H:%M:%S")
    mes+="\n中签号公布日及追缴日：%s\n祝您好运%c%c%c" % (lwrandate.strftime("%m月%d日"),sh_emoji,sh_emoji,sh_emoji)
except NameError:
    mes += "\n今日没有新股"

# 登录微信账号 开始发送
import itchat

itchat.auto_login(hotReload=True)#enableCmdQR=True
itchat.get_friends()
user = itchat.search_friends(name="霜Hyuk")
if user:
    itchat.send(mes, toUserName=user[0].get("UserName"))
# itchat.send(mes)
