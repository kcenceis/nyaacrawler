import re
from bs4 import BeautifulSoup

import Utils


def getImageURL(url, mBookTitle, count, total):
    r = Utils.getRequest(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for k in soup.find_all('img', class_='pic img img-responsive'):
        Utils.download_img_count(k["src"], mBookTitle, count, total)
        count += 1
