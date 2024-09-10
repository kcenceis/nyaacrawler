from SQL import Mysqldb, SQLitedb

# 模式为 MYSQL 和 SQLite
mode = "MYSQL"


def conn():
    if mode == "MYSQL":
        Mysqldb.conn()
        Mysqldb.DeleteSQL()
    elif mode =="SQLite":
        SQLitedb.connSQL()
        SQLitedb.DeleteSQL()

def isFinish(nyaa_list):
    if mode == "MYSQL":
        return Mysqldb.isFinish(nyaa_list)
    elif mode =="SQLite":
        return SQLitedb.isFinish(nyaa_list)

def HAS_SQL(nyaa_list):
    if mode == "MYSQL":
        return Mysqldb.HAS_SQL(nyaa_list)
    elif mode =="SQLite":
        return SQLitedb.HAS_SQL(nyaa_list)

def insertSQL(nyaa_list):
    if mode == "MYSQL":
        Mysqldb.insertSQL(nyaa_list)
    elif mode =="SQLite":
        SQLitedb.insertSQL(nyaa_list)

def updateSQL_Download(mADDRESS):
    if mode == "MYSQL":
        Mysqldb.updateSQL_Download(mADDRESS)
    elif mode =="SQLite":
        SQLitedb.updateSQL_Download(mADDRESS)

def isFinish_file_history(nyaa_list):
    if mode == "MYSQL":
        return Mysqldb.isFinish_file_history(nyaa_list)
    elif mode =="SQLite":
        return SQLitedb.isFinish_file_history(nyaa_list)

def isFinish_file_history_duplicate(nyaa_list):
    if mode == "MYSQL":
        return Mysqldb.isFinish_file_history_duplicate(nyaa_list)
    elif mode =="SQLite":
        return SQLitedb.isFinish_file_history_duplicate(nyaa_list)

def insertSQL_file_history(nyaa_list, url):
    if mode == "MYSQL":
        Mysqldb.insertSQL_file_history(nyaa_list, url)
    elif mode =="SQLite":
        SQLitedb.insertSQL_file_history(nyaa_list, url)

def updateSQL_http_history_information(nyaa_list):
    if mode == "MYSQL":
        Mysqldb.updateSQL_http_history_information(nyaa_list)
    elif mode =="SQLite":
        SQLitedb.updateSQL_http_history_information(nyaa_list)