import os
from urllib.parse import urlparse

from DrissionPage import SessionPage,SessionOptions

import SQLUTILS
import Utils


# pics4you imgsto picdollar imagebam silverpic premalo.com同架构
def get_image(url, nyaa_list):
    url_split = url.split('/')
    origin = url_split[0] + '//' + url_split[2]
    id = url_split[3]
    headers = {
        "origin": origin,
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "dnt": "1",
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
    }
    co = SessionOptions()
    co.set_headers(headers)
    page = SessionPage(co)
    page.post(url=url,data={
                            'op': 'view',
                            'id': id,
                            'pre': '1',
                            'next': 'Continue to image...'
                        })
    a = page.ele('tag:img@class=pic').attr('src')
    nyaa_list.file_name = Utils.filename_encode(a)
    page.download(a,nyaa_list.Path,nyaa_list.file_name)
    nyaa_list.count += 1
    SQLUTILS.insertSQL_file_history(nyaa_list, url)


    #r = requests.post(url,
    #                    headers=headers,
    #                    data={
    #                        'op': 'view',
    #                        'id': id,
    #                        'pre': '1',
    #                        'next': 'Continue to image...'
    #                    })
    #soup = BeautifulSoup(r.text, 'html.parser')
    #img_link = soup.find('img', class_='pic')['src']
    #Utils.download_img(img_link, nyaa_list)



