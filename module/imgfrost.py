import requests
import re
from bs4 import BeautifulSoup
import Utils


# type=0 imgfrost.net
# type=1 imgblaze.net
# 截取script中的document内容
def getImageURL(url, nyaa_list, type):
    if type == "0":
        # https://imgfrost.net 的url将会跳转至 http://imgair.net
        url = url.replace('://imgfrost.net', '://imgair.net')
    elif type == "1":
        url = url.replace('://imgblaze.net', '://imgair.net')
    # 开始请求
    req = Utils.getRequest(url)
    #print(req.text)
    soup = BeautifulSoup(req.text, 'html.parser')
    # 获取包含 document.location.href="https://prcf.imgbig.xyz/ 的字段
    # 2022/05/07修改
    pattern = re.compile(r"document.getElementById\(\"newImgE\"\)\.src = \"https://prcf.(.*?);$", re.MULTILINE | re.DOTALL)
    soup_document = soup.find_all('script', text=pattern)[0]
    # 获取字段中的http地址(即图片地址)
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
    url = re.findall(pattern, str(soup_document))
    print(url)
    Utils.download_img(url[0], nyaa_list)
