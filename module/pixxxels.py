import re

from bs4 import BeautifulSoup

import Utils


# 测试时先确认IP是否被屏蔽
# 请求是否成功 跟IP有关系？
def getImageURL(url, nyaa_list):
    r = Utils.getRequest(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    Utils.headers['referer'] = re.findall('http[s]?://[\w\W]{0,100}/', url)
    for k in soup.find_all('a', id='download'):
        Utils.download_img(k['href'], nyaa_list)


if __name__ == '__main__':
    url = ""
    getImageURL(url, nyaa_list="")
