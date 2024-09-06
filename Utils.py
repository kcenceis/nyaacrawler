import json
import os
import re
import time
from urllib.parse import urlparse

import mistune
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

import SQLUTILS
import main
from main import nyaa_list
from module import silverpic, hentaicovers, hentai4free, imgfrost, imagetwist, ibb, imgtaxi, pixxxels, xpic
import random
import string

from module.croea import croea
from module.imagehaha import imagehaha
from DrissionPage import ChromiumPage, ChromiumOptions

headers = {
    'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}

mReq = requests.session()
mReq.headers = headers
mReq.mount('https://', HTTPAdapter(max_retries=5))
mReq.mount('http://', HTTPAdapter(max_retries=5))
https_pattern = '(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Za-z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Za-z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Za-z0-9+&@#/%=~_|$?!:,.]*\)|[A-Za-z0-9+&@#/%=~_|$])'

co = ChromiumOptions()
co.incognito()  # 无痕模式
co.headless()  # 无头模式
# 设置UA
co.set_user_agent(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0')
co.set_argument('--no-sandbox')
co.set_argument('--window-size', '800,600')
co.set_argument('--start-maximized')
co.set_argument('--guest')
co.set_argument("--disable-gpu")
#co.set_proxy("http://10.1.2.253:2000")


# 进行下载图片 并且记录到数据库
# 图片的链接,nyaa_list
def download_img(url, nyaa_list):
    path = nyaa_list.Path + os.sep
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
            count = 0
            while response.status_code != 200:
                count += 1
                time.sleep(3)
                response = mReq.get(url)
                if count > 4:
                    pass
            img = response.content
            # 再判断是否有相同file_name
            # 无相同则直接用源文件名写入
            # 相同则随机生成一个文件名
            if not SQLUTILS.isFinish_file_history_duplicate(nyaa_list):
                with open(path + nyaa_list.file_name, 'wb') as g:
                    g.write(img)
                    g.writable()
                    SQLUTILS.insertSQL_file_history(nyaa_list, url)
            else:
                img_format = re.findall('\.(jpg|bmp|png|jpeg|webp|gif)', url)
                nyaa_list.file_name = str().join(
                    random.sample(string.ascii_letters + string.digits, 16)) + "." + img_format
                with open(path + nyaa_list.file_name, 'wb') as g:
                    g.write(img)
                    g.writable()
                    SQLUTILS.insertSQL_file_history(nyaa_list, url)
    except Exception as e:
        # 访问异常的错误编号和详细信息
        print(e.args)
        # print(str(e))
        # print(repr(e))
        pass
    # finally:
    #

# 定义Request方法,request headers 和 proxy
def getRequest(http_url):
    # 是否开启代理
    r = mReq.get(url=http_url, timeout=10)
    # r.raise_for_status()
    return r

# 将不能作为文件名的字符替换为下划线
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

# 连接并获取网页内容（第二页 即/view/111XXXX）
# 传入nyaa_list
def down(nyaa_list):
    page = ChromiumPage(co)
    print("将要进行抓取的网址:{}".format(nyaa_list.address))
    page.get(nyaa_list.address)
    for i in page.eles("tag:div@class=row"):
        # for x in i.eles("tag:div@class=row"):
        #    print(x.html)
        if re.search("Submitter:", i.html):
            # print(i.html)
            Submitter = [y.text for y in i.eles("tag:div@class=col-md-5")][0]
            nyaa_list.Submitter = Submitter
        elif re.search("Information:", i.html):
            Information = [y.text for y in i.eles("tag:div@class=col-md-5")][0]
            nyaa_list.Information = Information
    SQLUTILS.updateSQL_http_history_information(nyaa_list) # 写入Submitter information comments信息到数据
    process_url(page, nyaa_list)

def downimg(a,src,nyaa_list):
    nyaa_list.count += 1
    nyaa_list.file_name = os.path.basename(urlparse(src).path)
    a.save(path=nyaa_list.Path, name=nyaa_list.file_name)
    SQLUTILS.insertSQL_file_history(nyaa_list, src)

def process_url(page:ChromiumPage,nyaa_list:main.nyaa_list):
    torrent_text = page.eles('tag:div@id=torrent-description')
    print(nyaa_list.Information)
    tag_img = [item.eles('tag:img') for item in torrent_text]
    htmlurl_list = []
    if len(tag_img)>0:
        for i in tag_img[0]:
            src = i.attr('src')
            print("将要进行匹配的网址:{}".format(src))
            if re.search('^http[s]?://[\w\W]{0,2}hentai\.org/.*$', src):
                downimg(i,src,nyaa_list)
            elif re.search('^http[s]?://[\w\W]{0,2}\.wp\.com/.*$', src):
                downimg(i,src,nyaa_list)
            elif re.search('^http[s]?://i.imgur.com/.*.[jpg|bmp|png|jpeg|webp|gif]$', src):
                downimg(i,src,nyaa_list)
    html_url = [re.findall(https_pattern, item.html) for item in torrent_text]
    page.quit()
    if len(html_url) > 0:
        #print(html_url)
        for i in html_url[0]:
            if i not in htmlurl_list:
               htmlurl_list.append(i)
        for b in htmlurl_list:
            print("将要进行抓取的网址:{}".format(b))  # 抓取到的地址 将要进行抓取的网址
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
            # elif re.search('^http[s]?://pics4you.net/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
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
            elif re.search('^http[s]?://fotokiz.com/.*.html$', str_b):
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
            #elif re.search('^http[s]?://[\w\W]{0,2}imgur\.com/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
            #    download_img(b, nyaa_list)
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

            # 2022/05/07
            elif re.search('^http[s]?://[\w\W]{0,7}ckvwpzp.xyz/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                download_img(b, nyaa_list)
            elif re.search('^http[s]?://[\w\W]{0,7}imgxx.com/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                download_img(b, nyaa_list)
            elif re.search('^http[s]?://[\w\W]{0,12}imageshack.com/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                download_img(b, nyaa_list)
            elif re.search('^http[s]?://pics.dmm.co.jp/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                download_img(b, nyaa_list)

            # 2023/06/09
            # croea,imagehaha,imagexport为同个网页模板,服务端跟imagetwist有关系
            elif re.search('^http[s]?://[\w\W]{0,7}catbox.moe/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                download_img(b, nyaa_list)
            # 可能会卡死 不抓取diogo4d
            # elif re.search('^http[s]?://diogo4d.com/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
            #    download_img(b, nyaa_list)
            elif re.search('^http[s]?://imagehaha.com/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                imagehaha(str_b, nyaa_list)
            elif re.search('^http[s]?://croea.com/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                croea(str_b, nyaa_list)
            elif re.search('^http[s]?://imagexport.com/.*[jpg|bmp|png|jpeg|webp|gif]$', str_b):
                croea(str_b, nyaa_list)

            # 2024/1/15
            # 添加xpic支持
            elif re.search('http[s]?://xpic.org/', str_b):
                xpic.getImageURL(str_b, nyaa_list)
            # 添加postimg直连图片下载
            elif re.search('http[s]?://i.postimg.cc/', str_b):
                download_img(b, nyaa_list)

            # 不在抓取范围,结束抓取并记录
