import Utils
from SQL import SQLUtils


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
        SQLUtils.insertSQL_file_history(nyaa_list, imgUrl)
