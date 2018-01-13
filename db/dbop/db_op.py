import sqlite3

TYPE_SH = "Hu"
TYPE_HK = "Gang"
DB_NAME_SH = 'test_sh.db'
DB_NAME_HK = 'test_hk.db'
ERR_DB_BASE = 9000
ERR_DB_CONN = ERR_DB_BASE + 1
ERR_DB_CUR = ERR_DB_BASE + 2
ERR_DB_CONN_CLOSE = ERR_DB_BASE + 3
ERR_DB_CUR_CLOSE = ERR_DB_BASE + 4
ERR_DB_EXEC = ERR_DB_BASE + 5
ERR_DB_COMMIT = ERR_DB_BASE + 6
ERR_DB_FETALL = ERR_DB_BASE + 7
ERR_DB_NOT_EMPTY = ERR_DB_BASE + 8

RET_OK = 0

class db_op:
    def __init__(self, type):
        if type == TYPE_SH:
            self.db = DB_NAME_SH
        elif type == TYPE_HK:
            self.db = DB_NAME_HK
        else:
            self.db = DB_NAME_HK

    def db_connect(self):
        try:
            self.conn = sqlite3.connect(self.db)
        except:
            return ERR_DB_CONN
        return RET_OK

    def db_disconnect(self):
        try:
            self.conn.close()
        except:
            return ERR_DB_CONN_CLOSE
        return RET_OK

    def db_open_cur(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            return ERR_DB_CUR_CLOSE

        return RET_OK

    def db_close_cur(self):
        try:
            self.cursor.close()
        except:
            return ERR_DB_CUR

        return RET_OK

    def db_exec_sql(self, sql):
        try:
            #print(sql)
            self.cursor.execute(sql)
        except:
            return ERR_DB_EXEC
        return RET_OK

    def db_commit(self):
        try:
            self.conn.commit()
        except:
            return ERR_DB_COMMIT
        return RET_OK

    def db_fetall(self):
        try:
            values = self.cursor.fetchall()
        except:
            return ERR_DB_FETALL, []
        return RET_OK, values



