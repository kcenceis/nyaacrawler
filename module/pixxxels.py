from bs4 import BeautifulSoup

import Utils


def getImageURL(url, nyaa_list):
    r = Utils.getRequest(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for k in soup.find_all('a', id='download'):
        Utils.headers['referer'] = 'https://pixxxels.cc/'
        Utils.download_img(k['href'], nyaa_list)


if __name__ == '__main__':
    url = ""
    getImageURL(url, nyaa_list="")
