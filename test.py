from DrissionPage import ChromiumPage, ChromiumOptions
import re

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
    count = 0

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
# co.set_proxy("http://10.1.2.253:2000")
page = ChromiumPage(co)

page.get("https://sukebei.nyaa.si/view/4170491")
nyaa_list = nyaa_list()

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
nyaa_list.category = category
for i in page.eles("tag:div@class=row"):
    # for x in i.eles("tag:div@class=row"):
    #    print(x.html)
    if re.search("Submitter:", i.html):
        for y in i.eles("tag:a@class=text-success"):
            nyaa_list.Submitter = y.text
    elif re.search("Information:", i.html):
        Information = [y.text for y in i.eles("tag:div@class=col-md-5")][0]
        nyaa_list.Information = Information
Utils.process_url(page, nyaa_list)