import os

from DrissionPage import ChromiumPage, ChromiumOptions
import re

from DrissionPage._pages.session_page import SessionPage
from var_dump import var_dump

import Utils
from SQL import SQLUtils


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

url = "https://sukebei.nyaa.si/view/4184893"
SQLUtils.conn()
nyaa_list = nyaa_list()
nyaa_list.address = url
page = SessionPage()
# 访问目标网页
page.get(url)
ddd = page.eles("tag:div@class=panel-footer clearfix")
download_pattern = re.compile(r'/download/(?:[0-9])+.torrent')  # 种子pattern
magnet_pattern = re.compile(r'magnet:\?xt=urn:btih:')  # 磁链pattern
# 获取种子链接 磁链
for i in ddd:
    tag_a = i.eles('tag:a')
    for x in tag_a:
        href = x.attr('href')
        if re.search(download_pattern, href):
            nyaa_list.torrent = href
        if re.search(magnet_pattern, href):
            nyaa_list.magnet = href
# 获取标题 目录
for i in page.eles('tag:div@class=panel panel-default'):
    for k in i.eles('tag:h3@class=panel-title'):
        nyaa_list.title = k.text
# for i in page.eles('tag:div@class=panel panel-default'):
category = page.eles('tag:div@class=col-md-5')[0].eles('tag:a')[1].text
nyaa_list.Path = os.path.split(os.path.realpath(__file__))[0] + os.sep + category
nyaa_list.category = category
nyaa_list.Path = os.path.split(os.path.realpath(__file__))[0]+ os.sep + category
for i in page.eles("tag:div@class=row"):
    # for x in i.eles("tag:div@class=row"):
    #    print(x.html)
    if re.search("Submitter:", i.html):
        for y in i.eles("tag:a@class=text-success"):
            nyaa_list.Submitter = y.text
    elif re.search("Information:", i.html):
        Information = [y.text for y in i.eles("tag:div@class=col-md-5")][0]
        nyaa_list.Information = Information
Utils.down(nyaa_list)