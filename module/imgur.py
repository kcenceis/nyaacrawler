from DrissionPage import ChromiumPage, ChromiumOptions

import SQLUTILS


def download(url, nyaa_list):
    co = ChromiumOptions()
    co.incognito() # 无痕模式
    co.headless() # 无头模式
    #设置UA
    co.set_user_agent(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0')
    co.set_argument('--no-sandbox')
    co.set_argument('--window-size', '800,600')
    co.set_argument('--start-maximized')
    co.set_argument('--guest')
    co.set_argument("--disable-gpu")
    #co.set_proxy("http://10.1.2.253:2000")
    page = ChromiumPage(co)

    page.get(url)
    torrent_text=page.eles('#torrent-description')
    for i in torrent_text:
        for x in i.eles('tag:img'):
            print(x.attr('src'))
            x.save(r'.\imgs')
    nyaa_list.count += 1
    SQLUTILS.insertSQL_file_history(nyaa_list, url)
#for i in zx :
#    print(i)
#print(page.html)

co = ChromiumOptions()
co.incognito() # 无痕模式
co.headless() # 无头模式
#设置UA
co.set_user_agent(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0')
co.set_argument('--no-sandbox')
co.set_argument('--window-size', '1920,1080')
co.set_argument('--start-maximized')
co.set_argument('--guest')
co.set_argument("--disable-gpu")
#co.set_proxy("http://10.1.2.253:2000")
page = ChromiumPage(co)

page.get("https://i.imgur.com/efi9D5L.jpg")

print(page.html)
torrent_text=page.eles('tag:img')
for i in torrent_text:
    print(i.attr('src'))
    i.save(r'.\imgs')
print(torrent_text)
#for i in torrent_text:
#    for x in i.eles('tag:img'):
#        print(x.attr('src'))
#        x.save(r'.\imgs')