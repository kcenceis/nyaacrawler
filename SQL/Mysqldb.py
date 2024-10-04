import mysql.connector

host = "db"
user = ""
password = ""
db = "nyaacrawler"


def initMySQL():
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db
    )
    return mydb


# 传入数据表名称检查是否存在 返回True False
# param: 数据表名称
def check_database(database):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = mydb.cursor()
    database = (database,)
    sql = "SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = %s ;"
    cursor.execute(sql, database)
    if cursor.fetchone()[0] == 1:
        mydb.close()
        return True
    else:
        cursor.execute("CREATE DATABASE "+db)
        mydb.commit()
        mydb.close()
        return False


# 创建数据库
def conn():
    if not check_database(db):
        mydb = initMySQL()
        cursor = mydb.cursor()
        cursor.execute('''
        CREATE TABLE http_history                      
        (id INT PRIMARY KEY AUTO_INCREMENT,
        address        VARCHAR(200),
        title          VARCHAR(200),
        torrent        VARCHAR(200),
        magnet         text,
        category       VARCHAR(200),
        Submitter      text,
        Information    text,
        Comments       text,
        finish         INT(4),
        _delete         INT(4),
        dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data1          text,
        data2          text,
        data3          text,
        data4          text
        );
        ''')
        # 执行创建表
        cursor.execute('''
        CREATE TABLE file_history                      
       (id INT PRIMARY KEY AUTO_INCREMENT,
       nyaa_address   VARCHAR(200),
       file_name      VARCHAR(2000),
       count          INT(4),
       image_address  VARCHAR(200),
       dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       data1          text,
       data2          text,
       data3          text,
       data4          text
       );''')
        mydb.commit()
        mydb.close()


def insertSQL(nyaa_list):
    conn = initMySQL()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO http_history  (address,title,torrent,magnet,category,Submitter,Information,Comments) \
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                   (nyaa_list.address, nyaa_list.title, nyaa_list.torrent, nyaa_list.magnet, nyaa_list.category,
                    nyaa_list.Submitter, nyaa_list.Information, nyaa_list.Comments,))
    conn.commit()
    conn.close()


def insertSQL_file_history(nyaa_list, url):
    conn = initMySQL()
    cursor = conn.cursor()
    sql = "INSERT INTO file_history  (nyaa_address,file_name,count,image_address) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql, (nyaa_list.address, nyaa_list.file_name, nyaa_list.count, url,))
    conn.commit()
    conn.close()


# 获取有多少相同的地址，返回bool
def isFinish(nyaa_list):
    conn = initMySQL()
    cursor = conn.cursor()
    # 查询数据
    cursor.execute("SELECT count(*) as count  from http_history where address = %s and finish='1'",
                   (nyaa_list.address,))
    # values = cursor.fetchone()
    result = cursor.fetchone()[0]
    conn.close()
    if result == 1:
        return True
    else:
        return False


# 获取有多少相同的地址，返回bool
def isFinish_file_history(nyaa_list):
    conn = initMySQL()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) as count  from file_history where file_name = %s and nyaa_address = %s",
                   (nyaa_list.file_name, nyaa_list.address,))
    result = cursor.fetchone()[0]
    conn.close()
    if result == 1:
        return True
    else:
        return False


# 获取有多少相同的地址，返回bool
def isFinish_file_history_duplicate(nyaa_list):
    conn = initMySQL()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) as count  from file_history where file_name = %s", (nyaa_list.file_name,))
    # values = cursor.fetchone()
    result = cursor.fetchone()[0]
    conn.close()
    if result == 1:
        return True
    else:
        return False


# 获取count，查看是否存在相同条目，返回bool
def HAS_SQL(nyaa_list):
    conn = initMySQL()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) as count  from http_history where address = %s", (nyaa_list.address,))
    result = cursor.fetchone()[0]
    conn.close()
    if result == 1:
        return True
    else:
        return False


# 更新数据库，标识是否下载完毕
def updateSQL_http_history_information(nyaa_list):
    conn = initMySQL()
    cursor = conn.cursor()
    cursor.execute('''update http_history set Submitter=%s,Information=%s,Comments=%s where address= %s''',
                   (nyaa_list.Submitter, nyaa_list.Information, nyaa_list.Comments, nyaa_list.address,))
    conn.commit()
    cursor.close()
    conn.close()


# 更新数据库，标识是否下载完毕
def updateSQL_Download(mADDRESS):
    conn = initMySQL()
    cursor = conn.cursor()
    cursor.execute('''update http_history set finish='1' where address= %s''', (mADDRESS,))
    conn.commit()
    cursor.close()
    conn.close()


# 删除180日前的数据
def DeleteSQL():
    if check_database(db):
        conn = initMySQL()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM http_history WHERE dDate < DATE_SUB(NOW(), INTERVAL 180 DAY);")  # 删除180日之前的数据
        conn.commit()
        cursor.close()
        conn.close()
