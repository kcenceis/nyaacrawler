import requests
import SQLUTILS
import re
import os
import hentai4free
import hentaicovers
from requests.adapters import HTTPAdapter

import imagetwist
import imgfrost

proxyON = False  # 是否开启代理
filePath = os.path.split(os.path.realpath(__file__))[0]  # 获取脚本当前目录
# socks代理规则
proxies = {'http': 'socks5://127.0.0.1:1080',
           'https': 'socks5://127.0.0.1:1080'}
# Requests hearder
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/85.0.4183.83 Safari/537.36"}

mReq = requests.session()
mReq.mount('https://', HTTPAdapter(max_retries=3))
mReq.mount('http://', HTTPAdapter(max_retries=3))


def __init__(self):
    self._Directory = self


# url,标题
def download_img(url, title):
    path = filePath + os.sep + Directory + os.sep
    if not os.path.exists(path):
        os.mkdir(path)
    try:
        response = getRequest(url)
        img = response.content
        with open(path + title + r'.jpg', 'wb') as g:
            g.write(img)
            SQLUTILS.updateSQL_Download(title)
    except:
        pass


# 图片的URL,图片的标题，第几个url(用于标记title)，URL总数（用于判断是否已经完成)
def download_img_count(url, title, URLCOUNT, mUrl):
    path = filePath + os.sep + Directory + os.sep
    # print(URLCOUNT)
    # print(mUrl)
    if not os.path.exists(path):
        os.mkdir(path)
    try:
        response = getRequest(url)
        img = response.content
        with open(path + title + str(URLCOUNT) + r'.jpg', 'wb') as g:
            g.write(img)
            if mUrl == URLCOUNT:
                SQLUTILS.updateSQL_Download(title)
    except:
        pass


@property
def Directory(self):
    return self._Directory


@Directory.setter
def Directory(self, value):
    self._Directory = value


# 获取图片封面地址(第三页面)
# mSoup,第一页面提供的href
# mCount Title的列表位置
# mBoookTitle 第一页面所有Title(列表)
# 获取图片
def getBookCover(mSoup, mCount, mBookTitle):
    for stringSoup in mSoup.find_all('div', id='torrent-description'):
        # 获取地址https://hentai-covers.site/
        b = stringSoup.string  # 获取网页文中字段

        print(b)
        # b转换为str
        b = str(b)
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
        url = re.findall(pattern, b)
        if len(url) > 0:
            count = 1
            for b in url:
                # 识别NYAA网页内容,内容是否包含http
                if re.search('http', b):
                    # 只获取https://hentai-covers.site开头的网址
                    if re.search('https://hentai-covers.site', b):
                        hentaicovers.getImageURL(b, mBookTitle[mCount])
                    # 只获取https://hentai4free.net开头的网址
                    # b=图片url,mBookTitle[mCount]=图片标题,count=第几张图片,len(url)=url总数
                    elif re.search('https://hentai4free.net', b):
                        hentai4free.getImageURL(b, mBookTitle[mCount], count, len(url))
                    # 只获取https://imagetwist.com开头的网址
                    elif re.search('https://imagetwist.com', b):
                        imagetwist.getImageURL(b, mBookTitle[mCount], count, len(url))
                    elif re.search('https://imgfrost.net', b, "0"):
                        imgfrost.getImageURL(b, mBookTitle[mCount])
                    elif re.search('http://imgblaze.net', b, "1"):
                        imgfrost.getImageURL(b, mBookTitle[mCount])
                    # 不在抓取范围,结束抓取并记录
                    else:
                        SQLUTILS.updateSQL_Download(mBookTitle[mCount])
                # 不包含http,则直接结束抓取并记录
                else:
                    SQLUTILS.updateSQL_Download(mBookTitle[mCount])
                count += 1
        else:
            SQLUTILS.updateSQL_Download(mBookTitle[mCount])


# 定义Request方法,request headers 和 proxy
def getRequest(http_url):
    # 是否开启代理
    if proxyON:
        r = mReq.get(url=http_url, headers=headers, proxies=proxies, timeout=10)
    else:
        r = mReq.get(url=http_url, headers=headers, timeout=10)
    r.raise_for_status()
    return r
