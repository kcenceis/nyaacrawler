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
bookPageHtml = []  # 创建集合
bookTitle = []
# 获取第二页的地址和标题
for k in soup.find_all('a'):
    if re.search(r'#comments', k['href']):
        pass
    elif re.search(r'/view/', k['href']):
        mbookHTML = k['href']
        mTitle = re.sub('[\/:*?"<>|]', '-', str(k['title']))
        # 检查是否已经下载，未完成下载则加入列表
        if not SQLUTILS.countSQL(mbookHTML):
            bookPageHtml.append("https://sukebei.nyaa.si" + mbookHTML)
            bookTitle.append(mTitle)
            # 检查数据库是否已经有数据
            if not SQLUTILS.HAS_SQL(mbookHTML):
                SQLUTILS.insertSQL(mbookHTML, mTitle)  # 插入数据库
# 连接并获取网页内容（第二页）
for a in bookPageHtml:
    r = Utils.getRequest(a)
    print("地址:" + a)
    soup = BeautifulSoup(r.text, 'html.parser')
    Utils.getBookCover(soup, count, bookTitle)
    count += 1
