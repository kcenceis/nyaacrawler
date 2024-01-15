from bs4 import BeautifulSoup

import Utils


# 支持skviap.xyz doddbt.com
def get_image(url, nyaa_list):
    r = Utils.mReq.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    image = soup.find('input', id='embed-code-1')
    imageUrl = image['value']
    Utils.download_img(imageUrl, nyaa_list)
