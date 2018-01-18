import sqlite3
import time
import os
import shutil

TYPE_SH = "Hu"
TYPE_HK = "Gang"
TYPE_SZ = "Shen"
DB_NAME_SH = 'test_sh.db'
DB_NAME_HK = 'test_hk.db'
DB_NAME_SZ = 'test_sz.db'
DB_NAME_SH_BAK = DB_NAME_SH + '.bak'
DB_NAME_HK_BAK = DB_NAME_HK + '.bak'
DB_NAME_SZ_BAK = DB_NAME_SZ + '.bak'
tmp_dir = 'temp/'


ERR_DB_BASE = 300
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
            self.db_bak = DB_NAME_SH_BAK
        elif type == TYPE_HK:
            self.db = DB_NAME_HK
            self.db_bak = DB_NAME_HK_BAK
        elif type == TYPE_SZ:
            self.db = DB_NAME_SZ
            self.db_bak = DB_NAME_SZ_BAK
        else:
            self.db = DB_NAME_HK
            self.db_bak = DB_NAME_HK_BAK


    def back_up_db(self):
        self.db_close_cur()
        self.db_disconnect()

        # Create Temp/
        isTmpExists = os.path.exists(tmp_dir)
        if not isTmpExists:
            try:
                os.makedirs(tmp_dir)
            except:
                return -1

        # Copy to Temp
        if os.path.exists(self.db_bak):
            try:
                os.remove(self.db_bak)
            except:
                return -1
        try:
            shutil.copy(self.db, tmp_dir)
        except:
            return -1

        # Rename
        try:
            os.rename(tmp_dir + self.db, self.db_bak)
        except:
            return -1

        # remove
        os.removedirs(tmp_dir)
        return RET_OK

    def recover_db(self):
        self.db_close_cur()
        self.db_disconnect()

        # Check Backup File
        ifBakExists = os.path.exists(self.db_bak)
        if not ifBakExists:
            return -1

        # Remove Old DB
        if os.path.exists(self.db):
            try:
                os.remove(self.db)
            except:
                return -1

        # Rename
        try:
            os.rename(self.db_bak, self.db)
        except:
            return -1

        return RET_OK


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



