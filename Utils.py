import requests
import SQLUTILS
import re
import os
from requests.adapters import HTTPAdapter

import Utils
from module import silverpic, hentaicovers, hentai4free, imgfrost, imagetwist, ukkit, ibb, imgtaxi

proxyON = True  # 是否开启代理
filePath = os.path.split(os.path.realpath(__file__))[0]  # 获取脚本当前目录
# socks代理规则
proxies = {'http': 'socks5://127.0.0.1:1080',
           'https': 'socks5://127.0.0.1:1080'}
# Requests hearder
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                         "Chrome/85.0.4183.83 Safari/537.36"}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "dnt": "1",
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-dest': 'document',
    'upgrade-insecure-requests': '1'
}

mReq = requests.session()
mReq.mount('https://', HTTPAdapter(max_retries=5))
mReq.mount('http://', HTTPAdapter(max_retries=5))
# https_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
https_pattern = '(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Za-z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Za-z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Za-z0-9+&@#/%=~_|$?!:,.]*\)|[A-Za-z0-9+&@#/%=~_|$])'
# https_pattern = '(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Za-z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Za-z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Za-z0-9+&@#/%=~_|$?!:,.]*\)|[\u0000-\uFFFF]+|[A-Za-z0-9+&@#/%=~_|$])'
# torrent_img_pattern = '\]\((.+?)\)'
torrent_img_pattern = "http[s]?://(?:[a-zA-Z0-9]|[./])+"
count = 1


def __init__(self):
    self._Directory = self


# url,标题
def download_img(url, nyaa_list):
    path = filePath + os.sep + Directory + os.sep
    if not os.path.exists(path):
        os.mkdir(path)
    try:
        img_format = re.findall('\.(jpg|bmp|png|jpeg|webz|gif)', url)
        response = mReq.get(url)
        img = response.content
        if Utils.count > 1:
            nyaa_list.file_name = validateTitle(nyaa_list.title) + str(Utils.count) + '.' + img_format[0]
        else:
            nyaa_list.file_name = validateTitle(nyaa_list.title) + '.' + img_format[0]
        Utils.count = +1
        with open(path + nyaa_list.file_name, 'wb') as g:
            g.write(img)
            SQLUTILS.updateSQL_Download(nyaa_list.link)
            SQLUTILS.insertSQL_file_history(nyaa_list)

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
def getBookCover(mSoup, nyaa_list):
    for stringSoup in mSoup.find_all('div', id='torrent-description'):
        # 获取预览图地址
        b = stringSoup.string  # 获取网页文中字段

        print(b)
        # b转换为str
        b = str(b)
        Utils.count = 1
        url = re.findall(https_pattern, b)
        if len(url) > 0:
            for b in url:
                print("未处理的地址:{}".format(b))
                # 处理（https://aaaaa.com/XXX）带括号格式的地址
                #       if re.search(torrent_img_pattern, b):
                #           b = re.findall(torrent_img_pattern, b)
                #           print("处理后的地址:{}".format(b))
                #    for z in b:
                #        if re.search('(.*).(html|jpg|gif|png|bmp|webz|jpeg)', z):
                #            b = z
                #            print("处理后的地址:{}".format(b))
                str_b = str(b)
                # 文件名定义

                # 只获取https://hentai-covers.site开头的网址
                if re.search('https://hentai-covers.site', str_b):
                    hentaicovers.getImageURL(b, nyaa_list)
                # 只获取https://hentai4free.net开头的网址
                # b=图片url,mBookTitle[mCount]=图片标题,count=第几张图片,len(url)=url总数
                elif re.search('https://hentai4free.net', str_b):
                    hentai4free.getImageURL(b, nyaa_list)
                # 只获取https://imagetwist.com开头的网址6
                elif re.search('https://imagetwist.com', str_b):
                    imagetwist.getImageURL(b, nyaa_list)

                # 防止获取到缩略图 抓取5-11个字符之间的链接
                elif re.search('^http[s]?://imgfrost.net/\w{5,11}$', str_b):
                    imgfrost.getImageURL(b, nyaa_list, "0")
                elif re.search('^http[s]?://imgblaze.net/\w{5,11}$', str_b):
                    imgfrost.getImageURL(b, nyaa_list, "1")

                elif re.search('^http[s]?://ibb.co/.+?$', str_b):
                    ibb.get_image(b, nyaa_list)

                # imgtaxi.com imgadult.com
                elif re.search('^http[s]?://imgtaxi.com/.*.html$', str_b):
                    imgtaxi.get_image(b, nyaa_list)
                elif re.search('^http[s]?://imgadult.com/.*.html$', str_b):
                    imgtaxi.get_image(b, nyaa_list)

                # silverpic.com imgbaron.com pics4you.net picdollar.com premalo.com
                elif re.search('^https://silverpic.com/.*.html$', str_b):
                    silverpic.get_image(b, nyaa_list)
                elif re.search('^http[s]?://imgbaron.com/.*.html$', str_b):
                    silverpic.get_image(b, nyaa_list)
                # 中间匹配 数字+字母+下划线 10次以上 最后贪婪匹配所有 结尾.html
                elif re.search('^http[s]?://pics4you.net/\w{10,}/[\u0000-\uFFFF]+.html$', str_b):
                    silverpic.get_image(b, nyaa_list)
                elif re.search('^http[s]?://picdollar.com/.*.html$', str_b):
                    silverpic.get_image(b, nyaa_list)
                elif re.search('^http[s]?://premalo.com/.*.html$', str_b):
                    silverpic.get_image(b, nyaa_list)


                elif re.search('^http[s]?://ehgt.org.*[jpg|bmp|png|jpeg|webz|gif]$', str_b):
                    Utils.download_img(b, nyaa_list)


                # ukkit
                #  elif re.search('^http[s]?://skviap.xyz/v/.*$', str_b):
                #      ukkit.get_image(b,nyaa_list)
                #  elif re.search('^http[s]?://bvmqkla.de/v/.*$', str_b):
                #      ukkit.get_image(b, nyaa_list)
                #  elif re.search('^http[s]?://doddbt.com/v/.*$', str_b):
                #      ukkit.get_image(b, nyaa_list)

                elif re.search('^http[s]?://skviap.xyz.*[jpg|bmp|png|jpeg|webz|gif]$', str_b):
                    Utils.download_img(b, nyaa_list)
                elif re.search('^http[s]?://bvmqkla.de.*[jpg|bmp|png|jpeg|webz|gif]$', str_b):
                    Utils.download_img(b, nyaa_list)
                elif re.search('^http[s]?://doddbt.com.*[jpg|bmp|png|jpeg|webz|gif]$', str_b):
                    Utils.download_img(b, nyaa_list)

                elif re.search('^http[s]?://img.dlsite.jp/.*[jpg|bmp|png|jpeg|webz|gif]$', str_b):
                    Utils.download_img(b, nyaa_list)
                elif re.search('imagebam.com', str_b):
                    Utils.download_img(b, nyaa_list)
                elif re.search('^http[s]?://[\w\W]{0,2}imgur.com/.*[jpg|bmp|png|jpeg|webz|gif]$', str_b):
                    Utils.download_img(b, nyaa_list)
                elif re.search('^http[s]?://[\w\W]{0,7}caching.ovh/.*[jpg|bmp|png|jpeg|webz|gif]$', str_b):
                    Utils.download_img(b, nyaa_list)
                # 不在抓取范围,结束抓取并记录
                else:
                    SQLUTILS.updateSQL_Download(nyaa_list.link)

        else:
            SQLUTILS.updateSQL_Download(nyaa_list.link)


# 定义Request方法,request headers 和 proxy
def getRequest(http_url):
    # 是否开启代理
    if proxyON:
        r = mReq.get(url=http_url, headers=headers, proxies=proxies, timeout=10)
    else:
        r = mReq.get(url=http_url, headers=headers, timeout=10)
    # r.raise_for_status()
    return r


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
