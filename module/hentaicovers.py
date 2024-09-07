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


#from selenium import webdriver

def getImageURL(url, nyaa_list):
    # 获取封面 https://hentai-covers.site/images/2019/09/05/seiginoYbutachanbon.jpg
    # 获取图片网页链接
    url = url.replace(r'表紙 / Cover', '').replace('**', '').replace('Cover', '').strip()
    # 请求图片网页链接

    #    options = webdriver.EdgeOptions()
    #    options.use_chromium = True
    #    #options.add_argument('--headless')
    #    browser = webdriver.Edge(options=options)
    #    browser.get(url)
    #    # headers = browser.execute_script("return Object.assign({},window.performance.getEntries()[0].requestHeaders);")
    #    # print(headers)
    #    html = browser.page_source
    #    cookies = browser.get_cookies()
    #    cookies_list = [item["name"] + "=" + item["value"] for item in cookies]
    #    cookies = ';'.join(it for it in cookies_list)
    #    soup = BeautifulSoup(html, 'html.parser')
    #    #requestCover = requests.get(url,headers=headers,verify=False)
    #    #print(requestCover)
    #    ##  ^j^s ^o^vIMAGE ^|^=  ^~url
    #    #soup = BeautifulSoup(requestCover.text, 'html.parser')
    #    #print(soup)
    ##
    #    for kk in soup.find_all('link', rel='image_src'):
    #        print(kk['href'])
    #        download_img(kk['href'], nyaa_list, url,cookies)
    # for kk in soup.find_all('a', 'btn btn-download default'):
    #     print("测试kk:"+kk)
    #     # 下载图片
    #     Utils.download_img(kk['href'], mBookTitle)
    #from DrissionPage import ChromiumPage, ChromiumOptions
    #
    #co = ChromiumOptions()
    #co.headless()
    #page = ChromiumPage(co)
    #
    #page.get("https://hentai-covers.site/image/sAZs8")
    #print(page.html)
    #zx = page.eles('@rel=image_src')
    #cookies = page.cookies()
    #cookies_list = [item["name"] + "=" + item["value"] for item in cookies]
    #cookies = ';'.join(it for it in cookies_list)
    #print(zx.get.links()[0])
    #download_img(zx.get.links()[0],nyaa_list,url,cookies)
    #    from DrissionPage import ChromiumPage, ChromiumOptions
    #    co = ChromiumOptions()
    #    co.incognito()  # 无痕模式
    #    co.headless()  # 无头模式
    #    # 设置UA
    #    co.set_user_agent(
    #        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0')
    #    co.set_argument('--no-sandbox')
    #    co.set_argument('--window-size', '800,600')
    #    co.set_argument('--start-maximized')
    #    co.set_argument('--guest')
    #    co.set_argument("--disable-gpu")
    #    co.set_proxy("http://10.1.2.253:10111")
    #    page = ChromiumPage(co)
    Utils.page.get(url, retry=3, interval=2, timeout=15)
    #    print(page.html)
    imgUrl = ""
    for book in Utils.page.eles('.no-select cursor-zoom-in'):
        #print(book)
        # 获取封面图片对象
        # img = book('img')
        imgUrl = book.attr('src')
        nyaa_list.file_name = Utils.filename_encode(imgUrl)
        book.save(nyaa_list.Path,name=nyaa_list.file_name)
        print(imgUrl)
    #    page.quit()
    if nyaa_list.file_name != "":
        nyaa_list.count += 1
        SQLUTILS.insertSQL_file_history(nyaa_list, imgUrl)


def download_img(url, nyaa_list, hentaicovers_url, cookies):
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
        headers = {'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
                   'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                   'Sec-Fetch-Site': 'none', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1',
                   'Sec-Fetch-Dest': 'document', 'Accept-Encoding': 'gzip, deflate, br, zstd',
                   'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                   'Referer': hentaicovers_url,
                   'cookies': cookies
                   }
        print(headers)
        print(hentaicovers_url)
        if not SQLUTILS.isFinish_file_history(nyaa_list):
            nyaa_list.count += 1
            response = requests.get(url, timeout=10, verify=False)
            count = 0
            while response.status_code != 200:
                print("失败")
                count += 1
                time.sleep(3)
                response = requests.get(url, headers=headers, timeout=10, verify=False)
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
