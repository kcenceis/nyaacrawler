# nyaacatch

抓取sukeibei.nyaa预览图

Python version:3.7

## Table of Contents

- [Install_Requirements](#install_requirements)
- [Usage](#usage)
- [Maintainer](#maintainer)
- [License](#license)


# 现可抓取网址
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
* i.imgur.com
</pre>

## 数据库结构
SQLite: bookAddress.db

<div style=" display:table-cell; float:left;">
    <table>
        <tr>
            <td colspan="4" align="center">httphistory</td>
        </tr>
        <tr>
            <td>Column</td>
            <td>SQL Type</td>
            <td>Size</td>
            <td>PK</td>
        </tr>
        <tr>
            <td>ID</td>
            <td>INTEGER</td>
            <td></td>
            <td>PK</td>
        </tr>
        <tr>
            <td>ADDRESS</td>
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
            <td>ID</td>
            <td>INTEGER</td>
            <td></td>
            <td>PK</td>
        </tr>
        <tr>
            <td>ADDRESS</td>
            <td>CHAR</td>
            <td>50</td>
            <td></td>
        </tr>
        <tr>
            <td>TITLE</td>
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
            <td>MAGNET</td>
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

## Install_Requirements

pip install -r requirements.txt

## Usage

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

## Maintainer

[@kcenceis](https://github.com/kcenceis)

## License

[GNU General Public License v3.0](LICENSE)
