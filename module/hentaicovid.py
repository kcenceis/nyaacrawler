from DrissionPage import SessionPage,SessionOptions

from SQL import SQLUtils


def get_image(url, nyaa_list):
    co = SessionOptions()
    #    co.set_headers(headers)
    page = SessionPage(co)
    page.get(url)
    img_html = page.ele('tag:div@class=fileviewer-file').ele('tag:img')
    page.download(img_html.attr('src'), nyaa_list.Path, nyaa_list.file_name)
    nyaa_list.count += 1
    SQLUtils.insertSQL_file_history(nyaa_list, url)

#test
#get_image("https://hentaicovid.com/uploads/x9hqSOTP1KhWWBp-FC2-PPV-4587645.jpg")