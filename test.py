import re
import SQLUTILS
import Utils

download_pattern = re.compile(r'/download/(?:[0-9])+.torrent')  # 种子pattern
magnet_pattern = re.compile(r'magnet:\?xt=urn:btih:')  # 磁链pattern
file_category = "Games"


class nyaa_list:
    address = ''
    title = ''
    torrent = ''
    magnet = ''
    category = ''
    file_name = ''
    count = 0


SQLUTILS.connSQL()  # 检查是否存在数据库
SQLUTILS.DeleteSQL()  # 清除旧数据
i = nyaa_list()
i.address = "https://sukebei.nyaa.si/view/3638858"
i.title = "abc"
i.torrent = "https://sukebei.nyaa.si/download/3636728.torrent"
i.magnet = "magnet:?xt=urn:btih:31080702eb9701a1205621467007ef2014a02419&dn=Pingping%20-%20Kaine.zip&tr=http%3A%2F%2Fsukebei.tracker.wf%3A8888%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"
i.category = "Real_Life_Video"
Utils.down(i)
