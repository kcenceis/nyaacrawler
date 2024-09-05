from bs4 import BeautifulSoup
import Utils

# pics4you imgsto picdollar imagebam silverpic premalo.com同架构
def get_image(url, nyaa_list):
    url_split = url.split('/')
    origin = url_split[0] + '//' + url_split[2]
    id = url_split[3]
    #img_name = url_split[4].replace('.html', '')
    headers = {
        "origin": origin,
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "dnt": "1",
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
    }
    r = Utils.mReq.post(url,
                        headers=headers,
                        data={
                            'op': 'view',
                            'id': id,
                            'pre': '1',
                            'next': 'Continue to image...'
                        })
    soup = BeautifulSoup(r.text, 'html.parser')
    img_link = soup.find('img', class_='pic')['src']
    Utils.download_img(img_link, nyaa_list)



