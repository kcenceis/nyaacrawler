import re

import mistune
import requests
from bs4 import BeautifulSoup

import Utils
from module import xpic

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                        "Chrome/114.0.0.0 Safari/537.36"
headers['Content-Type'] = "application/x-www-form-urlencoded"
headers['sec-ch-ua'] = '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"'
mReq = requests.session()
mReq.headers = headers
https_pattern = '(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Za-z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Za-z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Za-z0-9+&@#/%=~_|$?!:,.]*\)|[A-Za-z0-9+&@#/%=~_|$])'


r = mReq.get("https://sukebei.nyaa.si/view/4025043")
mSoup = BeautifulSoup(r.text, 'html.parser')
for stringSoup in mSoup.find_all('div',class_='panel-body'):
    #print(len(stringSoup))
    for i in stringSoup.find_all('div',class_='row'):
        if re.search('Information:',str(i)):
            print(i.find('a',rel='noopener noreferrer nofollow').text)

for stringSoup in mSoup.find_all('div', id='torrent-description'):
    b = stringSoup.string  # 获取网页文中字段
    # b转换为str
    b = str(b)
    b = mistune.html(b)
    print(b)
    url = re.findall(https_pattern, b)
    print(url)
    for b in url:
        print("将要进行抓取的网址:{}".format(b))  # 抓取到的地址 将要进行抓取的网址
        str_b = str(b)
        if re.search('http[s]?://[\w\W]{0,7}postimg.cc/', str_b):
            #xpic.getImageURL(str_b)
            print(str_b)
            r = mReq.get(str_b)
            soup = BeautifulSoup(r.text, 'html.parser')
            #mReq.headers['referer'] = re.findall('http[s]?://[\w\W]{0,100}/', str(url))
            print(soup)
            #for k in soup.find_all('a', id='download'):
            #    print(k)
#print(r.text)