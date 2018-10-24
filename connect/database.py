# coding: utf-8
#import pymysql
#pymysql.install_as_MySQLdb()
import MySQLdb
from . import prepare



def check(userID):

    conn = prepare.init()

    c = conn.cursor()
    sql = "SELECT state FROM checked_list WHERE userID=\'{0}\'".format(userID)
    c.execute(sql)

    result = c.fetchall()
    c.close()

    if len(result) == 0: return '***'
    return result[0][0]


def select(sql):

    conn = prepare.init()
    c = conn.cursor()
    c.execute(sql)
    result = c.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return result

def update(database, values):

    conn = prepare.init()
    c = conn.cursor()

    if database == 'checked_list':
        c.execute('UPDATE checked_list SET state = \'' + values[0] +'\' WHERE userID= \'' + values[1] + '\'')
    elif database == 'api_limit':
        c.execute('UPDATE api_limit SET limited = \'' + str(values[1]) +'\', last_use = \'' + values[2] + '\' WHERE api_name = \'' + values[3] + '\' and id = \'' + str(values[0]) + '\'')
    else:
        print("database is failed")
    # データベースへの変更を保存
    conn.commit()
    c.close()
    conn.close()


def insert(database, values):

    conn = prepare.init()
    c = conn.cursor()
    s = ','.join( ["%s"]*len(values))
    s = "(" + s + ")"

    # レコードの登録
    sql = 'INSERT ignore into {0} values {1}'.format(database, s)
    if isinstance(values,tuple): c.execute(sql, values)  # 1件のみ
    else: c.executemany(sql, values)    # 複数件

    # データベースへの変更を保存
    conn.commit()

    c.close()
    conn.close()
