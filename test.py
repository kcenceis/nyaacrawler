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
i.address = ""
i.title = ""
i.torrent = ""
i.magnet = ""
i.category = ""
Utils.down(i)
