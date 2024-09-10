from DrissionPage import SessionPage
import Utils
from SQL import SQLUtils


def getImageURL(url, nyaa_list):
    page = SessionPage()
    page.get(url)
    x = page.ele('tag:img@class=pic img img-responsive')
    img_url = x.attr('src')
    nyaa_list.file_name = Utils.filename_encode(img_url)
    page.download(img_url,nyaa_list.Path,nyaa_list.file_name)
    if nyaa_list.file_name !="":
       nyaa_list.count += 1
       SQLUtils.insertSQL_file_history(nyaa_list, img_url)
    #r = Utils.getRequest(url)
    #soup = BeautifulSoup(r.text, 'html.parser')
    #for k in soup.find_all('img', class_='pic img img-responsive'):
    #    Utils.download_img(k["src"], nyaa_list)
