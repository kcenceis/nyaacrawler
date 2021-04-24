from bs4 import BeautifulSoup

import Utils


def getImageURL(imageURL, mBookTitle, count, total):
    #   # 以空格分开多个URL，变成集合
    #   url = mUrlist.split()
    #   # 定义文件的次数
    #   count = 1
    #   # 获取图片真实地址
    r = Utils.getRequest(imageURL)
    soup = BeautifulSoup(r.text, 'html.parser')
    count = 1
    # for k in soup.find_all('meta',property='og:image'):

    # 下载图片
    for k in soup.find_all('link', rel='image_src'):
        Utils.download_img(k['href'], mBookTitle + count, total)
        count += 1
