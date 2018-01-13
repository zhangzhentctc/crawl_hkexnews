import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import sqlite3
import time

def create_table_day():
    sql = "create table stock_day(day date primary key not null,mark int)"
    conn = sqlite3.connect('test0.db')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except:
        print("Create Table Day Fail")

def create_table_info():
    sql = "create table stock_info(code int primary key not null,name varchar(50))"
    conn = sqlite3.connect('test0.db')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except:
        print("Create Table Day Fail")

def create_table_vol():
    sql = "create table stock_vol(id integer primary key autoincrement,code int not null,day date not null,volume int,percent real)"
    conn = sqlite3.connect('test0.db')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except:
        print("Create Table Day Fail")


def create_bls():
    create_table_day()
    create_table_info()
    create_table_vol()

def test_insert():
    conn = sqlite3.connect('test0.db')
    # 创建一个Cursor:
    cursor = conn.cursor()
    # 执行一条SQL语句，创建user表:
    try:
        cursor.execute('create table stockday (day date PRIMARY KEY NOT NULL, mark int)')
    except:
        pass
    dates=[]
    # 继续执行一条SQL语句，插入一条记录:
    for date in dates:
        sql = "insert into stockday (day, mark) values (" + \
              "'" + date + "'" + "," + \
              "'" + "1" + "'" + \
              ")"
        print(sql)
        cursor.execute(sql)
    #sql = "insert into stock_vol(code, day, volume, percent) values(999876, '2017-12-03',100,0.0003)"
    #cursor.execute(sql)
    # 通过rowcount获得插入的行数:
    print(cursor.rowcount)
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()

def test_query():
    times = time.time()
    conn = sqlite3.connect('test.db')
    timee = time.time()
    print("Connect:" + str(timee - times))

    times = time.time()
    cursor = conn.cursor()
    timee = time.time()
    print("Cursor:" + str(timee - times))

    # 执行查询语句:
    #cursor.execute('select * from user where id=?', ('1',))
    cursor.execute("SELECT * FROM stockday")
    #cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    #
    # 获得查询结果集:
    values = cursor.fetchall()
    print(values)
    cursor.close()
    conn.close()

#test_insert()
#create_bls()
test_query()
