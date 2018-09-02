import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
from lxml.html import fromstring
from itertools import cycle
import pygsheets as pg
ivThreshold = 50 #Set Min IV = 50
#Pushing to Gsheet
gs = pg.authorize(service_file='YOUR_CREDENTIAL_FILE.json')
try:
    gs.delete("PCR")
except:
    sh = gs.create("PCR")
sh=gs.open("PCR")
sh.share('anyone', role='reader', expirationTime=None, is_group=False)
sh.share('YOUR_EMAIL_HERE', role='writer', expirationTime=None, is_group=False)
try:
    wsIV = sh.worksheet_by_title("PCR")
except:
    wsIV = sh.add_worksheet(title="PCR", rows="1", cols="5")
values = ['Stock','Call OI','Put OI','PCR','Comment']
for x in range(5):
    wsIV.update_cell((1,x+1), values[x])
#Fetch Proxies
def get_proxies():
    url = 'https://www.sslproxies.org/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies
proxies = get_proxies()
#print(proxies)
proxy_pool = cycle(proxies)
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

#Fetch FNO Stocks
fnoStocks = []
url= 'https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/foSecStockWatch.json'
#Get a proxy from the pool
proxy = next(proxy_pool)
user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}
r = requests.get(url,headers = headers,proxies={"http": proxy, "https": proxy})
data = r.json()
fnoStocks = []
stockList = data['data']
for symbol in stockList:
    fno = (symbol['symbol'])
    fnoStocks.append(fno)
fnoStocks.sort()
print(len(fnoStocks))
#print(fnoStocks)
col_list_head = ['Stock','Call OI','Put OI','PCR','Comment']

data_Req = []
count = 0
for stock in fnoStocks:
    count+=1
    Base_url =(f"https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=2772&symbol={stock}&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17")
    r= requests.get(Base_url,headers = headers,proxies={"http": proxy, "https": proxy})

    data = r.text
    #print(data)

    soup = BeautifulSoup(data, "html.parser")
    all_table_row = soup.find_all('tr')

    all_table_row_list = []
    tdf = pd.DataFrame(columns=col_list_head)
    row_marker = 0
    for i in all_table_row:
        all_table_row_list.append(i.text)

    #print(all_table_row_list)
    last_row = all_table_row_list[-2]
    last_row_list = last_row.split('\n')

    call_value = last_row_list[2][1:]
    if call_value == "" or call_value == 'hart':
        call_value = "0"
    call_value = call_value.replace(',',"")
    print("call value: "+call_value)
    call_value = int(call_value)



    print(type(call_value))

    put_value = last_row_list[-3][1:]
    if put_value == "" or put_value == 'I':
        put_value = "0"
    put_value = put_value.replace(",","")
    put_value = int(put_value)
    print(type(put_value))
    if call_value == 0 or put_value == 0:
        pcr = 0
    else:
        pcr = put_value/call_value
    pcr = round(pcr,2)
    if put_value > call_value:
        comment = "Go Long! But don't forget to short a call option"
    else:
        comment = "Short em down! But don't forget to short a put option"
    tdf.at[row_marker,'Stock']= stock
    tdf.at[row_marker,'Call OI']= call_value
    tdf.at[row_marker,'Put OI']= put_value
    tdf.at[row_marker,'PCR']= pcr
    tdf.at[row_marker,'Comment']= comment
    row_marker += 1
    #print(tdf.dropna())
    data_Req.append(tdf.dropna())
    print(count)
result = pd.concat(data_Req)

# Write to gsheet
wsIV.set_dataframe(result,'A1', copy_index=False, copy_head=True, fit=True, escape_formulae=False)
