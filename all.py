import os
import re
import sys

import Utils
from DrissionPage import SessionPage

from SQL import SQLUtils

Nyaa_DOMAIN = 'https://sukebei.nyaa.si'
url_list = {
"Anime":Nyaa_DOMAIN + "/?f=0&c=1_1&q=",
"Doujinshi":Nyaa_DOMAIN + "/?f=0&c=1_2&q=",
"Games":Nyaa_DOMAIN + "/?f=0&c=1_3&q=",
"Manga":Nyaa_DOMAIN + '/?f=0&c=1_4&q=',
"Picture": Nyaa_DOMAIN + '/?f=0&c=1_5&q=',
"Real_Life_Photo":Nyaa_DOMAIN + '/?f=0&c=2_1&q=',
"Real_Life_Video":Nyaa_DOMAIN + '/?f=0&c=2_2&q='}


class nyaa_list:
    address = ''
    title = ''
    torrent = ''
    magnet = ''
    category = ''
    file_name = ''
    Information = ''
    Submitter = ''
    Comments = ''
    Path = ''
    count = 0


# 生成nyaa_list 抓取 sukeibe.nyaa 目录 中的 链接 标题 磁链 种子
def init_nyaalist(page_,category):
    s = nyaa_list()
    s.category = category
    s.Path = os.path.split(os.path.realpath(__file__))[0] + os.sep + category
    for i in page_.eles('tag:a'):
        if re.search(download_pattern, str(i)):
            s.torrent = i.attr('href')
        if re.search(magnet_pattern, str(i)):
            s.magnet = i.attr('href')
        if re.search(r'/view/', str(i)):
            #s.address = Nyaa_DOMAIN + i.attr('href')
            s.address = i.attr('href')
            s.title = i.attr('title')
    return s

SQLUtils.conn()
# 以s模式创建页面对象
page = SessionPage()
download_pattern = re.compile(r'/download/(?:[0-9])+.torrent')  # 种子pattern
magnet_pattern = re.compile(r'magnet:\?xt=urn:btih:')  # 磁链pattern
for category,url in url_list.items():
    # 访问目标网页
    page.get(url)
    book_list = []  # 创建集合2
    # 获取<tr class='success'>中的所有内容
    for k in page.eles('tag:tr@class=success'):
        book_list.append(init_nyaalist(k,category))

    # 获取<tr class='default'>中的所有内容
    for k in page.eles('tag:tr@class=default'):
        book_list.append(init_nyaalist(k,category))

    # i 为 nyaa_list
    for i in book_list:
        # 检查是否已经下载完成
        # |_未完成
        #  |_数据库不存在该条目 则创建该条目 并下载
        #  |_数据库存在该条目 直接下载
        try:
            if not SQLUtils.isFinish(i):
                # 检查数据库是否已经有数据 没有则插入数据
                if not SQLUtils.HAS_SQL(i):
                    SQLUtils.insertSQL(i)  # 插入数据库
                    # 连接并获取网页内容（第二页）
                    Utils.down(i)
                # 查询是否已经抓取过 但并没有下载到图片 再重新抓取一次
                # 返回True则数据并没有下载成功
                # elif SQLUTILS.isFinish_download_finish(i):
                #    Utils.down(i)
                # 有数据则直接下载
                else:
                    # 连接并获取网页内容（第二页）
                    Utils.down(i)
            # 循环完成后写入完成
            SQLUtils.updateSQL_Download(i.address)
        except KeyboardInterrupt as e:
            sys.exit()
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            exception_info = "Exception Type: {}\nException Object: {}\nLine Number: {}\nURL:{}".format(exc_type,
                                                                                                        exc_obj,
                                                                                                        exc_tb.tb_lineno,
                                                                                                        i.address)
            # 将异常信息写入到文件中
            with open("error.log", "a") as file:
                file.write(exception_info)
            continue






