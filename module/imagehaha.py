import requests
from bs4 import BeautifulSoup

import Utils


def imagehaha(url,nyaa_list):
    requestCover = requests.get(url)
    # 抓取IMAGE真实url
    soup = BeautifulSoup(requestCover.text, 'html.parser')
    # print(soup)
    k = soup.find('div', id='tab3')
    Utils.download_img(k.find('img')['src'],nyaa_list)