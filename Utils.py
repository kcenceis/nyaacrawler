import os
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

import SQLUTILS
from module import silverpic, hentaicovers, hentai4free, imgfrost, imagetwist, ibb, imgtaxi, pixxxels
import random
import string

proxyON = False  # 是否开启代理
filePath = os.path.split(os.path.realpath(__file__))[0]  # 获取脚本当前目录
# socks代理规则
proxies = {'http': 'socks5://127.0.0.1:1080',
           'https': 'socks5://127.0.0.1:1080'}

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                        "Chrome/90.0.4430.93 Safari/537.36 "
headers['Content-Type'] = "application/x-www-form-urlencoded"
headers['dnt'] = "1"
headers['sec-ch-ua'] = '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
headers['sec-fetch-site'] = 'same-origin'
headers['sec-fetch-dest'] = 'document'
headers['upgrade-insecure-requests'] = '1'

mReq = requests.session()
mReq.mount('https://', HTTPAdapter(max_retries=5))
mReq.mount('http://', HTTPAdapter(max_retries=5))
https_pattern = '(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Za-z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Za-z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Za-z0-9+&@#/%=~_|$?!:,.]*\)|[A-Za-z0-9+&@#/%=~_|$])'


# 进行下载图片 并且记录到数据库
# 图片的链接,nyaa_list
def download_img(url, nyaa_list):
    path = filePath + os.sep + nyaa_list.category + os.sep
    if not os.path.exists(path):
        os.mkdir(path)
    try:
        # if nyaa_list.count > 1:
        #    nyaa_list.file_name = validateTitle(nyaa_list.title) + str(nyaa_list.count) + '.' + img_format[0]
        # else:
        #    nyaa_list.file_name = validateTitle(nyaa_list.title) + '.' + img_format[0]
        nyaa_list.file_name = os.path.basename(urlparse(url).path)
        # 检查file_history中是否已经存在该文件名 不存在则进行下载
        # 原因：同一个页面中多张相同文件名的图片 同一个页面的相同图片不再下载
        # 1.精确匹配 相同address file_name则不下载（排除了同页面多次下载同文件
        #   2.再模糊查询 相同file_name就改名
        if not SQLUTILS.isFinish_file_history(nyaa_list):
            nyaa_list.count += 1
            response = mReq.get(url)
            img = response.content
            # 再判断是否有相同file_name
            # 无相同则直接用源文件名写入
            # 相同则随机生成一个文件名
            if not SQLUTILS.isFinish_file_history_duplicate(nyaa_list):
                   with open(path + nyaa_list.file_name, 'wb') as g:
                       g.write(img)
                       g.writable()
                       SQLUTILS.updateSQL_Download(nyaa_list.address)
                       SQLUTILS.insertSQL_file_history(nyaa_list)
            else:
                img_format = re.findall('\.(jpg|bmp|png|jpeg|webp|gif)', url)
                nyaa_list.file_name = str().join(random.sample(string.ascii_letters + string.digits, 16))+"."+img_format
                with open(path + nyaa_list.file_name, 'wb') as g:
                    g.write(img)
                    g.writable()
                    SQLUTILS.updateSQL_Download(nyaa_list.address)
                    SQLUTILS.insertSQL_file_history(nyaa_list)

    except:
        pass


# 连接并获取网页内容（第二页 即/view/111XXXX）
# 传入nyaa_list
def down(nyaa_list):
    r = getRequest(nyaa_list.address)
    print("地址:" + nyaa_list.address)
    soup = BeautifulSoup(r.text, 'html.parser')
    getBookCover(soup, nyaa_list)


# 抓取图片封面地址 分析是何种图片网站 使用模块 下载图片
# mSoup,第二页的网站内容
# nyaa_list
def getBookCover(mSoup, nyaa_list):
    for stringSoup in mSoup.find_all('div', id='torrent-description'):
        b = stringSoup.string  # 获取网页文中字段
        print(b)
        # b转换为str
        b = str(b)
        url = re.findall(https_pattern, b)
        if len(url) > 0:
            for b in url:
                print("未处理的地址:{}".format(b))  # 抓取到的地址 将要进行抓取的网址
                str_b = str(b)
                # 文件名定义

                # 只获取https://hentai-covers.site开头的网址
                if re.search('https://hentai-covers.site', str_b):
                    hentaicovers.getImageURL(b, nyaa_list)
                # 只获取https://hentai4free.net开头的网址
                # b=图片url,mBookTitle[mCount]=图片标题,count=第几张图片,len(url)=url总数
                elif re.search('https://hentai4free.net', str_b):
                    hentai4free.getImageURL(b, nyaa_list)
                # 只获取https://imagetwist.com开头的网址
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
                # small 改成 big 类的图站
                elif re.search('^http[s]?://imgtaxi.com/.*.html$', str_b):
                    imgtaxi.get_image(b, nyaa_list)
                elif re.search('^http[s]?://imgadult.com/.*.html$', str_b):
                    imgtaxi.get_image(b, nyaa_list)
                elif re.search('^http[s]?://imgdrive.net/.*.html$', str_b):
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
                elif re.search('^http[s]?://fotokiz.com/.*.html$', str_b):
                    silverpic.get_image(b, nyaa_list)
                elif re.search('^http[s]?://imgsen.com/.*.html$', str_b):
                    silverpic.get_image(b, nyaa_list)
                elif re.search('^http[s]?://imgsto.com/.*.html$', str_b):
                    silverpic.get_image(b, nyaa_list)
                elif re.search('^http[s]?://imgstar.eu/.*.html$', str_b):
                    silverpic.get_image(b, nyaa_list)


                elif re.search('^http[s]?://ehgt.org.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)


                # ukkit
                #  elif re.search('^http[s]?://skviap.xyz/v/.*$', str_b):
                #      ukkit.get_image(b,nyaa_list)
                #  elif re.search('^http[s]?://bvmqkla.de/v/.*$', str_b):
                #      ukkit.get_image(b, nyaa_list)
                #  elif re.search('^http[s]?://doddbt.com/v/.*$', str_b):
                #      ukkit.get_image(b, nyaa_list)

                elif re.search('^http[s]?://skviap.xyz.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)
                elif re.search('^http[s]?://bvmqkla.de.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)
                elif re.search('^http[s]?://doddbt.com.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)

                elif re.search('^http[s]?://img.dlsite.jp/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)
                elif re.search('imagebam.com', str_b):
                    download_img(b, nyaa_list)
                elif re.search('^http[s]?://[\w\W]{0,2}imgur\.com/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)
                elif re.search('^http[s]?://[\w\W]{0,7}caching\.ovh/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)

                elif re.search('^http[s]?://[\w\W]{0,7}turboimg\.net/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)

                # 2022/5/5新增
                elif re.search('http[s]?://pixxxels.cc/', str_b):
                    pixxxels.getImageURL(b, nyaa_list)
                elif re.search('http[s]?://postimg.cc/', str_b):
                    pixxxels.getImageURL(b, nyaa_list)

                elif re.search('^http[s]?://[\w\W]{0,7}ax21pics.net/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)
                elif re.search('^http[s]?://[\w\W]{0,7}catbox\.moe/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)

                # 2022/05/07
                elif re.search('^http[s]?://[\w\W]{0,7}ckvwpzp.xyz/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)
                elif re.search('^http[s]?://[\w\W]{0,7}imgxx.com/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)
                elif re.search('^http[s]?://[\w\W]{0,12}imageshack.com/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)
                elif re.search('^http[s]?://pics.dmm.co.jp/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                    download_img(b, nyaa_list)
                # 不在抓取范围,结束抓取并记录
                else:
                    SQLUTILS.updateSQL_Download(nyaa_list.address)

        else:
            SQLUTILS.updateSQL_Download(nyaa_list.address)


# 定义Request方法,request headers 和 proxy
def getRequest(http_url):
    # 是否开启代理
    if proxyON:
        r = mReq.get(url=http_url, headers=headers, proxies=proxies, timeout=10)
    else:
        r = mReq.get(url=http_url, headers=headers, timeout=10)
    # r.raise_for_status()
    return r


# 将不能作为文件名的字符替换为下划线
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
