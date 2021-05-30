import requests
from bs4 import BeautifulSoup

import Utils


# imgtaxi.com imgadult.com
def get_image(url, nyaa_list):
    # 请求
    r = requests.get(url)
    # 抓取预览图
    soup = BeautifulSoup(r.text, 'html.parser')
    i = soup.find('meta', property='og:image')
    new_str = str(i['content'])
    # 替换字段
    image_link = new_str.replace('/small/', '/big/')
    # 下载
    Utils.download_img(image_link, nyaa_list)
