# nyaacrawler

抓取sukeibei.nyaa预览图

Python version:3.9

## 内容

- [现可抓取网址](#现可抓取网址)
- [数据库设计](#数据库设计)
- [安装](#安装)
- [使用方法](#使用方法)
- [维护人](#维护人)
- [许可](#许可)

## 现可抓取网址
<pre>
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
* imgur.com
* caching.ovh
</pre>

## 数据库设计
SQLite: bookAddress.db

<div style=" display:table-cell; float:left;">
    <table>
        <tr>
            <td colspan="4" align="center">http_history</td>
        </tr>
        <tr>
            <td>Column</td>
            <td>SQL Type</td>
            <td>Size</td>
            <td>PK</td>
        </tr>
        <tr>
            <td>id</td>
            <td>INTEGER</td>
            <td></td>
            <td>PK</td>
        </tr>
        <tr>
            <td>address</td>
            <td>CHAR</td>
            <td>50</td>
            <td></td>
        </tr>
        <tr>
            <td>finish</td>
            <td>INT</td>
            <td>4</td>
            <td></td>
        </tr>
        <tr>
            <td>dDate</td>
            <td>TIMESTAMP</td>
            <td></td>
            <td></td>
        </tr>
    </table>
</div>

<div style="  display:table-cell;float:left;">
    <table>
        <tr>
            <td colspan="4" align="center">file_history</td>
        </tr>
        <tr>
            <td>Column</td>
            <td>SQL Type</td>
            <td>Size</td>
            <td>PK</td>
        </tr>
        <tr>
            <td>id</td>
            <td>INTEGER</td>
            <td></td>
            <td>PK</td>
        </tr>
        <tr>
            <td>address</td>
            <td>CHAR</td>
            <td>50</td>
            <td></td>
        </tr>
        <tr>
            <td>title</td>
            <td>CHAR</td>
            <td>200</td>
            <td></td>
        </tr>
        <tr>
            <td>torrent</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>magnet</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>category</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>file_name</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>dDate</td>
            <td>TIMESTAMP</td>
            <td></td>
            <td></td>
        </tr>
    </table>
</div>

## 安装

git clone https://github.com/kcenceis/nyaacrawler.git

pip install -r requirements.txt

## 使用方法

开启socks代理方法:修改Utils.py中的proxyON为True

<div style="  display:table-cell; ">
<table>
  <tr>
       <td></td>
       <td>Command</td>
  </tr>
  <tr>
       <td>Anime</td>
       <td>python main.py 1</td>
  </tr>
  <tr>
       <td>Doujinshi</td>
       <td>python main.py 2</td>
  </tr>
  <tr>
       <td>Games</td>
       <td>python main.py 3</td>
  </tr>
  <tr>
       <td>Manga</td>
       <td>python main.py 4</td>
  </tr>
  <tr>
       <td>Picture</td>
       <td>python main.py 5</td>
  </tr>
  <tr>
       <td>Photo</td>
       <td>python main.py 6</td>
  </tr>
</table>
</div>

## 维护人

[@kcenceis](https://github.com/kcenceis)

## 许可

[GNU General Public License v3.0](LICENSE)
