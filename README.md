# nyaacatch

抓取sukeibei.nyaa预览图

Python version:3.7

# 现可抓取网址

* hentai-covers.site

* hentai4free.net
* imagetwist.com

* imgfrost.net
* imgblaze.net

* ibb.co

* imgtaxi.com
* imgadult.com

* silverpic.com
* imgbaron.com
* pics4you.net
* picdollar.com
* premalo.com

* ehgt.org
* skviap.xyz
* bvmqkla.de
* doddbt.com
* img.dlsite.jp
* imagebam.com
* i.imgur.com

## 安装依赖

pip install -r requirements.txt

## 数据库结构
<pre>
SQLite: bookAddress.db

TABLE:
httphistory
|----ID      自动ID
|----ADDRESS 网页链接
|----finish  下载完成
|____dDate   写入数据库的时间

TABLE:
file_history
|----ID       自动ID
|----ADDRESS  网页链接
|----TITLE    网页标题
|----torrent  种子下载地址
|----MAGNET   磁链下载地址
|----file_name预览图文件名
|____dDate    写入数据库的时间
</pre

## 使用方法

开启socks代理方法:修改Utils.py中的proxyON为True

* 抓取Anime
  * python main.py 1
* 抓取Doujinshi
  * python main.py.py 2
* 抓取Games
  * python main.py.py 3
* 抓取Manga
  * python main.py.py 4
* 抓取Picture
  * python main.py.py 5
* 抓取Photo
  * python main.py.py 5
