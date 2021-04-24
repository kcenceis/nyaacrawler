from bs4 import BeautifulSoup

import Utils


def getImageURL(url, mBookTitle, total):
    r = Utils.getRequest(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    count = 1
    for k in soup.find_all('img', class_='pic img img-responsive'):
        Utils.download_img(k["src"], mBookTitle+count, total)
        count += 1
