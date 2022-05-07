from bs4 import BeautifulSoup

import Utils


def get_image(url,nyaa_url):
    r = Utils.getRequest(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    i = soup.find('div', id='image-viewer-container')
    image_url = i.find('img')['src']
    Utils.download_img(image_url,nyaa_url)
