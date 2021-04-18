import sqlite3
import os

SQLDATABASEFILE = os.path.split(os.path.realpath(__file__))[0]+os.sep+'bookAddress.db'  # 数据库文件名称


def connSQL():
    if not os.path.exists(SQLDATABASEFILE):  # 检查是否存在表
        conn = sqlite3.connect(SQLDATABASEFILE)
        print('Opened database successfully');
        c = conn.cursor()

        # 执行创建表
        c.execute('''CREATE TABLE httphistory                      
       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
       ADDRESS        CHAR(50),
       TITLE          CHAR(200),
       finish         INT(4),
       dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );''')
        # 插入数据表
        conn.commit()
        c.close()
        conn.close()


def insertSQL(mAddress, mTitle):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    c.execute("INSERT INTO httphistory (ADDRESS,TITLE) \
      VALUES (?,?)", (mAddress, mTitle,));
    conn.commit()
    c.close()
    conn.close()


def selectSQL():
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    conn.commit()
    # 查询数据
    cursor = c.execute("SELECT *  from httphistory")
    for row in cursor:
        print("ID = ", row[0])
        print("ADDRESS = ", row[1])
    cursor.close()
    conn.close()


# 获取有多少相同的地址，返回bool
def countSQL(mAddress):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    # 查询数据
    cursor = c.execute("SELECT count(*) as count  from httphistory where ADDRESS = ? and finish='1'", (mAddress,))
    # values = cursor.fetchone()
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if result == 1:
        return True
    else:
        return False


# 获取count，查看是否存在相同条目，返回bool
def HAS_SQL(mAddress):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    # 查询数据
    cursor = c.execute("SELECT count(*) as count  from httphistory where ADDRESS = ?", (mAddress,))
    # values = cursor.fetchone()
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if result == 1:
        return True
    else:
        return False


# 更新数据库，标识是否下载完毕
def updateSQL_Download(mTITLE):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    cursor = c.execute('''update httphistory set finish='1' where TITLE= ?''', (mTITLE,))
    conn.commit()
    cursor.close()
    conn.close()


# 删除7日前的数据
def DeleteSQL():
    if os.path.exists(SQLDATABASEFILE):
        conn = sqlite3.connect(SQLDATABASEFILE)
        c = conn.cursor()
        cursor = c.execute("delete from httphistory where date('now', '-7 day') >= date(dDate)")  # 删除7日前的数据
        conn.commit()
        cursor.close()
        conn.close()
