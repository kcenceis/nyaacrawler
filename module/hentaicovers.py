import os
import random
import re
import string
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

import SQLUTILS
import Utils


def getImageURL(url, nyaa_list):
    # 获取封面 https://hentai-covers.site/images/2019/09/05/seiginoYbutachanbon.jpg
    # 获取图片网页链接
    url = url.replace(r'表紙 / Cover', '').replace('**', '').replace('Cover', '').strip()
    # 请求图片网页链接
    requestCover = Utils.getRequest(url)
    # 抓取IMAGE真实url
    soup = BeautifulSoup(requestCover.text, 'html.parser')
    for kk in soup.find_all('link', rel='image_src'):
        download_img(kk['href'], nyaa_list)
    # for kk in soup.find_all('a', 'btn btn-download default'):
    #     print("测试kk:"+kk)
    #     # 下载图片
    #     Utils.download_img(kk['href'], mBookTitle)


headers = {}
headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                        "Chrome/114.0.0.0 Safari/537.36"
headers['sec-ch-ua'] = '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"'


def download_img(url, nyaa_list):
    path = Utils.filePath + os.sep + nyaa_list.category + os.sep
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
            response = requests.get(url, headers=headers)
            count = 0
            while response.status_code != 200:
                print("失败")
                count += 1
                time.sleep(3)
                response = requests.get(url, headers=headers)
                if count > 5:
                    break
            img = response.content
            # 再判断是否有相同file_name
            # 无相同则直接用源文件名写入
            # 相同则随机生成一个文件名
            if not SQLUTILS.isFinish_file_history_duplicate(nyaa_list):
                with open(path + nyaa_list.file_name, 'wb') as g:
                    g.write(img)
                    g.writable()
                    SQLUTILS.updateSQL_Download(nyaa_list.address)
                    SQLUTILS.insertSQL_file_history(nyaa_list,url)
            else:
                img_format = re.findall('\.(jpg|bmp|png|jpeg|webp|gif)', url)
                nyaa_list.file_name = str().join(
                    random.sample(string.ascii_letters + string.digits, 16)) + "." + img_format
                with open(path + nyaa_list.file_name, 'wb') as g:
                    g.write(img)
                    g.writable()
                    SQLUTILS.updateSQL_Download(nyaa_list.address)
                    SQLUTILS.insertSQL_file_history(nyaa_list,url)
    except Exception as e:
        # 访问异常的错误编号和详细信息
        print(e.args)
        # print(str(e))
        # print(repr(e))
        pass
