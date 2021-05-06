from bs4 import BeautifulSoup

import Utils


def getImageURL(mUrlist, nyaa_list):
    count = 0
    if len(mUrlist) > 1:
        count = 1
    for i in mUrlist:
        r = Utils.getRequest(i)
        soup = BeautifulSoup(r.text, 'html.parser')
        # for k in soup.find_all('meta',property='og:image'):

        # 下载图片
        for k in soup.find_all('link', rel='image_src'):
            if count == 0:
                Utils.download_img(k['href'], nyaa_list)
            else:
                nyaa_list.title = nyaa_list.title + count
                Utils.download_img(k['href'], nyaa_list)
                count += 1
