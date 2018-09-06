
import sqlite3

def CreateDB(db_name,sqlTable):
    conn = sqlite3.connect(db_name)
    try:
        cursor = conn.cursor()
        cursor.execute(sqlTable)
    except:
        print("创建失败,或已存在")
    cursor.close()

def insterDB(db_name,sql):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    
def insterDB_item(db_name,sql,item):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql,item)
    conn.commit()
    cursor.close()

def selectDB(db_name,sql):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    results = cursor.execute(sql)
    return results.fetchall()

