import os
import re
import sys

import Utils
from DrissionPage import SessionPage

from SQL import SQLUtils

Nyaa_DOMAIN = 'https://sukebei.nyaa.si'
url_Art_Anime = Nyaa_DOMAIN + "/?f=0&c=1_1&q="  # Anime
url_Art_Doujinshi = Nyaa_DOMAIN + "/?f=0&c=1_2&q="  # 同人志
url_Art_Games = Nyaa_DOMAIN + "/?f=0&c=1_3&q="  # 游戏
url_Art_Manga = Nyaa_DOMAIN + '/?f=0&c=1_4&q='  # 漫画
url_Art_Picture = Nyaa_DOMAIN + '/?f=0&c=1_5&q='  # 图片
url_Real_Life_Photo = Nyaa_DOMAIN + '/?f=0&c=2_1&q='  # Real_Life - Photobooks and Pictures
url_Real_Life_Video = Nyaa_DOMAIN + '/?f=0&c=2_2&q='
argvalue = sys.argv[1:]


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
def init_nyaalist(page_):
    s = nyaa_list()
    s.category = file_category
    s.Path = os.path.split(os.path.realpath(__file__))[0] + os.sep + file_category
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


if __name__ == '__main__':
    if len(argvalue) != 0:
        if argvalue[0] == "1":
            url = url_Art_Anime
            file_category = 'Anime'
        elif argvalue[0] == '2':
            url = url_Art_Doujinshi
            file_category = 'Doujinshi'
        elif argvalue[0] == '3':
            url = url_Art_Games
            file_category = 'Games'
        elif argvalue[0] == '4':
            url = url_Art_Manga
            file_category = 'Manga'
        elif argvalue[0] == '5':
            url = url_Art_Picture
            file_category = 'Picture'
        elif argvalue[0] == '6':
            url = url_Real_Life_Photo
            file_category = 'Real_Life_Photo'
        elif argvalue[0] == '7':
            url = url_Real_Life_Video
            file_category = 'Real_Life_Video'
        else:
            print('退出程序')
            sys.exit()
    else:
        print('选择抓取数据页面:\n'
              '1:Anime\n'
              '2:Doujinshi\n'
              '3:Games\n'
              '4:Manga\n'
              '5:Picture\n'
              '6:Real Life_Photo\n'
              '7:Real Life_Video\n'
              )
        urlChoose = input('选择:')

        if urlChoose == '1':
            url = url_Art_Anime
            file_category = 'Anime'
        elif urlChoose == '2':
            url = url_Art_Doujinshi
            file_category = 'Doujinshi'
        elif urlChoose == '3':
            url = url_Art_Games
            file_category = 'Games'
        elif urlChoose == '4':
            url = url_Art_Manga
            file_category = 'Manga'
        elif urlChoose == '5':
            url = url_Art_Picture
            file_category = 'Picture'
        elif urlChoose == '6':
            url = url_Real_Life_Photo
            file_category = 'Real_Life_Photo'
        elif urlChoose == '7':
            url = url_Real_Life_Video
            file_category = 'Real_Life_Video'
        else:
            print('退出程序')
            sys.exit()
    #SQLUTILS.connSQL()  # 检查是否存在数据库
    #SQLUTILS.DeleteSQL()  # 清除旧数据
    #r = Utils.getRequest(url)  # 请求第一个页面
    #soup = BeautifulSoup(r.text, 'html.parser')
    SQLUtils.conn()
    # 以s模式创建页面对象
    page = SessionPage()
    # 访问目标网页
    page.get(url)

    download_pattern = re.compile(r'/download/(?:[0-9])+.torrent')  # 种子pattern
    magnet_pattern = re.compile(r'magnet:\?xt=urn:btih:')  # 磁链pattern

    book_list = []  # 创建集合2
    # 获取<tr class='success'>中的所有内容
    for k in page.eles('tag:tr@class=success'):
        book_list.append(init_nyaalist(k))

    # 获取<tr class='default'>中的所有内容
    for k in page.eles('tag:tr@class=default'):
        book_list.append(init_nyaalist(k))

    # danger代表不能运行,甚至有可能是病毒 不建议抓取 预留条目
    ## 获取<tr class='danger'>中的所有内容
    # for k in soup.find_all('tr', class_='danger'):
    #    book_list.append(init_nyaalist(k))

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
                #elif SQLUTILS.isFinish_download_finish(i):
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
            exception_info = "Exception Type: {}\nException Object: {}\nLine Number: {}\nURL:{}\n".format(exc_type,exc_obj,exc_tb.tb_lineno,i.address)
            # 将异常信息写入到文件中
            with open(os.path.split(os.path.realpath(__file__))[0]+os.sep+"error.log", "a") as file:
                file.write(exception_info)
            continue
    Utils.page.quit()
