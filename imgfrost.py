import requests
import re
from bs4 import BeautifulSoup
import Utils

# 截取script中的document内容
def getImageURL(mUrlist, mBookTitle):
    # https://imgfrost.net 的url将会跳转至 http://imgair.net
    new_mUrllist = str(mUrlist).replace('https://imgfrost.net', 'http://imgair.net')
    # 开始请求
    req = Utils.getRequest(new_mUrllist)
    soup = BeautifulSoup(req.text, 'html.parser')
    # 获取包含 document.location.href="https://prcf.imgbig.xyz/ 的字段
    pattern = re.compile(r"document.location.href=\"https://prcf.imgbig.xyz/(.*?);$", re.MULTILINE | re.DOTALL)
    soup_document = soup.find_all('script', text=pattern)[0]
    # 获取字段中的http地址(即图片地址)
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
    url = re.findall(pattern, str(soup_document))
    Utils.download_img(url[0], mBookTitle)
