from bs4 import BeautifulSoup

import Utils


def getImageURL(url, nyaa_list):
    r = Utils.getRequest(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # for k in soup.find_all('meta',property='og:image'):
    # 下载图片
    for k in soup.find_all('link', rel='image_src'):
        Utils.download_img(k['href'], nyaa_list)
