import os

import requests
from bs4 import BeautifulSoup

import Utils


def getImageURL(url,nyaa_list):
    r = requests.get(url)
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(r.text)
    k = soup.find('div', class_='img-inner dark')
    imgUrl = k.find('img')['src']
    Utils.download_img(imgUrl, nyaa_list)
