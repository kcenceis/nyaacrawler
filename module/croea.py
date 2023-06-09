import requests
from bs4 import BeautifulSoup
import Utils


def croea(url,nyaa_list):
    requestCover = requests.get(url)
    # 抓取IMAGE真实url
    soup = BeautifulSoup(requestCover.text, 'html.parser')
    k = soup.find('a', class_='ddownloader')
    Utils.download_img(k['href'], nyaa_list)