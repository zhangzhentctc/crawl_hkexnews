import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import sqlite3


def test_insert():
    conn = sqlite3.connect('test.db')
    # 创建一个Cursor:
    cursor = conn.cursor()
    # 执行一条SQL语句，创建user表:
    #cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')

    # 继续执行一条SQL语句，插入一条记录:
    sql = "insert into user (id, name) values (" + \
          "'" + "2" + "'" + "," + \
          "'" + "Aaron" + "'" + \
          ")"
    print(sql)
    cursor.execute(sql)

    # 通过rowcount获得插入的行数:
    print(cursor.rowcount)
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()

def test_query():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # 执行查询语句:
    #cursor.execute('select * from user where id=?', ('1',))
    cursor.execute('select * from user')
    # 获得查询结果集:
    values = cursor.fetchall()
    print(values)
    cursor.close()
    conn.close()

#test_insert()
test_query()
