from bs4 import BeautifulSoup

import Utils


def getImageURL(mUrlist, nyaa_list):
    count = 0
    if len(mUrlist) > 1:
        count = 1
    for i in mUrlist:
        r = Utils.getRequest(i)
        soup = BeautifulSoup(r.text, 'html.parser')
        for k in soup.find_all('img', class_='pic img img-responsive'):
            if count == 0:
                Utils.download_img(k["src"], nyaa_list)
            else:
                nyaa_list.title = nyaa_list.title + count
                Utils.download_img(k["src"], nyaa_list)
                count += 1
