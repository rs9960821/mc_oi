import requests
import csv
from lxml import etree
import datetime
import os

today = datetime.datetime.now()
date_list = []
dataList = []
for date in range(30):
    yesterday = today - datetime.timedelta(days=date) 
    days = yesterday.strftime('%Y/%m/%d')
    url = 'https://www.taifex.com.tw/cht/3/futContractsDate'
    payload = {'queryType': '3', 'goDay':'', 'doQuery': '1','dateaddcnt': '1','queryDate': days}
    r = requests.post(url, data=payload)
    r.encoding = 'utf-8'
    html = r.text
    data = etree.HTML(html)
    a_list = data.xpath('//*[@id="printhere"]/div[4]/table/tbody/tr[2]/td/table/tbody/tr[6]/td[12]/div[1]/font')
    date = data.xpath('//*[@id="printhere"]/div[4]/table/tbody/tr[1]/td/p/span[2]')
    
    for i, j in zip(a_list, date):
        i = i.text.strip()
        dateString = j.text
        data = [dateString[2:], '0', '0', '0', i]
        dataList.append(data)

if os.path.isfile('./oi.csv'):
    with open('oi.csv', newline='') as f:
        reader = csv.reader(f)
        for line in reader:
            date_list.append(line[0])
else:
    with open('oi.csv', 'a', newline='') as f: 
        writer = csv.writer(f)
        writer.writerow(['date', 'open', 'high', 'low', 'close'])

for i in range(len(dataList)-1,-1,-1):
    with open('oi.csv', 'a', newline='') as f:
        if dataList[i][0] in date_list:
            continue
        else: 
            writer = csv.writer(f)
            writer.writerow(dataList[i])
f.close()
