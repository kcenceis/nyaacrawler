from bs4 import BeautifulSoup

import Utils


def getImageURL(url, nyaa_list):
    r = Utils.getRequest(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for k in soup.find_all('img', class_='pic img img-responsive'):
        Utils.download_img(k["src"], nyaa_list)
