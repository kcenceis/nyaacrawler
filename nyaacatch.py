import re
import sys
from bs4 import BeautifulSoup

import SQLUTILS
import Utils

urlDoujinshi = "https://sukebei.nyaa.si/?f=0&c=1_2&q="  # 同人志
urlManga = 'https://sukebei.nyaa.si/?f=0&c=1_4&q='  # 漫画
urlPicture = 'https://sukebei.nyaa.si/?f=0&c=1_5&q='  # 图片
count = 0
count2 = 0
argvalue = sys.argv[1:]


class nyaa_list:
    title = ''
    link = ''
    torrent = ''
    magnet = ''


def down(i):
    r = Utils.getRequest("https://sukebei.nyaa.si" + i.link)
    print("地址:" + i.link)
    soup = BeautifulSoup(r.text, 'html.parser')
    Utils.getBookCover(soup, i)


if len(argvalue) != 0:
    if argvalue[0] == "1":
        url = urlDoujinshi
        Utils.Directory = 'Donjinshi'
    elif argvalue[0] == '2':
        url = urlManga
        Utils.Directory = 'Manga'
    elif argvalue[0] == '3':
        url = urlPicture
        Utils.Directory = 'Picture'
    else:
        print('退出程序')
        sys.exit()
else:
    print('选择抓取数据页面:\n'
          '1:同人志\n'
          '2:漫画\n'
          '3:图片')
    urlChoose = input('选择:')

    if urlChoose == '1':
        url = urlDoujinshi
        Utils.Directory = 'Donjinshi'
    elif urlChoose == '2':
        url = urlManga
        Utils.Directory = 'Manga'
    elif urlChoose == '3':
        url = urlPicture
        Utils.Directory = 'Picture'
    else:
        print('退出程序')
        sys.exit()
SQLUTILS.connSQL()  # 检查是否存在数据库
SQLUTILS.DeleteSQL()  # 清除旧数据
r = Utils.getRequest(url)  # 请求第一个页面

soup = BeautifulSoup(r.text, 'html.parser')

download_pattern = re.compile(r'/download/(?:[0-9])+.torrent')  # 种子pattern
magnet_pattern = re.compile(r'magnet:\?xt=urn:btih:')  # 磁链pattern

book_list = []  # 创建集合
# 获取<tr class='success'>中的所有内容
for k in soup.find_all('tr', class_='success'):
    s = nyaa_list()
    for i in k.find_all('a'):
        if re.search(download_pattern, str(i)):
            s.torrent = i['href']
        if re.search(magnet_pattern, str(i)):
            s.magnet = i['href']
        if re.search(r'/view/', str(i)):
            s.link = i['href']
            s.title = i['title']
    book_list.append(s)

for i in book_list:
    # 检查是否已经下载完成
    # |_未完成
    #  |_数据库不存在该条目 则创建该条目 并下载
    #  |_数据库存在该条目 直接下载
    if not SQLUTILS.isFinish(i.link):
        # 检查数据库是否已经有数据 没有则插入数据
        if not SQLUTILS.HAS_SQL(i.link):
            SQLUTILS.insertSQL(i.link)  # 插入数据库
            # 连接并获取网页内容（第二页）
            down(i)
        # 有数据则直接下载
        else:
            # 连接并获取网页内容（第二页）
            down(i)
