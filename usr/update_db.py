##
## Function: Download data that we do not have from web
## Input:  data
## Output: None

from crawls.crawl import *
from db.db_agency import *
import threading



ENGLISH = 1
CHINESE = 2

language = CHINESE

STR_UPDB_IDLE = "Idle"
STR_UPDB_INIT_DB = "Init Database"
STR_UPDB_GET_EMPTY_DAYS = "Get Empty Days"
STR_UPDB_CRAWL = "Crawling "
STR_UPDB_STORE = "Storing "
STR_UPDB_OK = "Crawling OK "
STR_UPDB_ALL_OK = "Crawling OK "
STR_UPDB_TIMEOUT = "Some days missing due to network  "
STR_UPDB_ERR = "Crawling ERR "
STR_STOCK_MKT_NAME_SH = "SH"
STR_STOCK_MKT_NAME_SZ = "SZ"
STR_STOCK_MKT_NAME_HK = "HK"

if language == ENGLISH:
    STR_UPDB_IDLE = "Idle"
    STR_UPDB_INIT_DB = "Init Database"
    STR_UPDB_GET_EMPTY_DAYS = "Get Empty Days"
    STR_UPDB_CRAWL = "Crawling "
    STR_UPDB_STORE = "Storing "
    STR_UPDB_OK = "Crawling OK "
    STR_UPDB_ALL_OK = "Crawling OK "
    STR_UPDB_TIMEOUT = "Some days missing due to network  "
    STR_UPDB_ERR = "Crawling ERR "
    STR_STOCK_MKT_NAME_SH = "SH "
    STR_STOCK_MKT_NAME_SZ = "SZ "
    STR_STOCK_MKT_NAME_HK = "HK "

if language == CHINESE:
    STR_UPDB_IDLE = "爬虫：空闲"
    STR_UPDB_INIT_DB = "爬虫：初始化数据库"
    STR_UPDB_GET_EMPTY_DAYS = "爬虫：获取空白日期"
    STR_UPDB_CRAWL = "爬虫：抓取信息... "
    STR_UPDB_STORE = "爬虫：存储信息... "
    STR_UPDB_OK = "爬虫：完成 "
    STR_UPDB_ALL_OK = "爬虫：所有完成 "
    STR_UPDB_TIMEOUT = "由于网络问题丢失了一些交易日，请再次更新"
    STR_UPDB_ERR = "爬虫：错误 编号 "
    STR_STOCK_MKT_NAME_SH = "沪 "
    STR_STOCK_MKT_NAME_SZ = "深 "
    STR_STOCK_MKT_NAME_HK = "港 "



TYPE_NAME_LIST = [STR_STOCK_MKT_NAME_HK, STR_STOCK_MKT_NAME_SH, STR_STOCK_MKT_NAME_SZ]

TYPE_SH = "Hu"
TYPE_HK = "Gang"
TYPE_SZ = "Shen"
TYPE_LIST = [TYPE_HK, TYPE_SH, TYPE_SZ]



class update_db(threading.Thread):
    def __init__(self, type, callback):
        super(update_db, self).__init__()
        self.status_text = STR_UPDB_IDLE
        self.stock_type = type
        self.stopped = False
        self.callback = callback
        self.havetimeout = False

    def init_db(self):
        self.db_agen = db_agency(self.stock_type)

        ret = self.db_agen.init_db_tl()
        if ret != RET_OK:
            return ret

        ret = self.db_agen.check_db_normal()
        if ret != RET_OK:
            ret_ = self.db_agen.recover_db()
            if ret_ != RET_OK:
                return ret_
            # if it recovers, init it again
            self.db_agen = db_agency(self.stock_type)
            ret = self.db_agen.init_db_tl()
            if ret != RET_OK:
                return ret

        ret = self.db_agen.backup_db()
        if ret != RET_OK:
            return ret
        return RET_OK

    def get_empty_days(self):

        ret, list = self.db_agen.get_hungry_days()
        if ret != RET_OK:
            return ret

        self.empty_days = list
        return RET_OK

    def update_info(self):
        bad_days = []
        for day in self.empty_days:
            if self.stopped == True:
                return -1
            self.status_text = STR_UPDB_CRAWL+ str(self.stock_type_name) + str(day)
            crawl_t = crawl(day, self.stock_type)
            ret = crawl_t.crawl_process()
            if ret == ERR_CRAWL_DATE_MATCH:
                ret = self.db_agen.mark_day_rest(day)
                if ret != RET_OK:
                    self.update_err(ret)
                    continue
            elif ret == RET_OK:
                self.status_text = STR_UPDB_STORE+ str(self.stock_type_name) + str(day)
                ret = self.db_agen.store_day_data(day, crawl_t.stock_tl)
                if ret != RET_OK:
                    self.update_err(ret)
                    continue
            else:
                self.update_err(ret)
                bad_days.append(day)
                continue

        for day in bad_days:
            if self.stopped == True:
                return -1
            self.status_text = STR_UPDB_CRAWL+ str(self.stock_type_name) + str(day)
            crawl_t = crawl(day, self.stock_type)
            ret = crawl_t.crawl_process()
            if ret == ERR_CRAWL_DATE_MATCH:
                ret = self.db_agen.mark_day_rest(day)
                if ret != RET_OK:
                    self.update_err(ret)
                    continue
            elif ret == RET_OK:
                self.status_text = STR_UPDB_STORE+ str(self.stock_type_name) + str(day)
                ret = self.db_agen.store_day_data(day, crawl_t.stock_tl)
                if ret != RET_OK:
                    self.update_err(ret)
                    continue
            elif ret == ERR_SELENIUM_GET_TIMEOUT:
                self.havetimeout = True
                continue
            else:
                return -1

        return RET_OK


    def update_process(self):
        self.status_text = STR_UPDB_INIT_DB + str(self.stock_type_name)
        ret = self.init_db()
        if ret != RET_OK:
            self.status_text = STR_UPDB_ERR + str(self.stock_type_name) + str(ret)
            return ret

        self.status_text = STR_UPDB_GET_EMPTY_DAYS
        ret = self.get_empty_days()
        if ret != RET_OK:
            self.status_text = STR_UPDB_ERR + str(self.stock_type_name) + str(ret)
            return ret

        ret = self.update_info()
        if ret != RET_OK:
            self.status_text = STR_UPDB_ERR + str(self.stock_type_name) + str(ret)
            return ret

        self.status_text = str(self.stock_type_name) + STR_UPDB_OK
        return RET_OK

    def get_update_status(self):
        return self.status_text

    def update_err(self, ret):
        print(ret)

    def run(self):
        self.stopped = False
        for i in range(0, 3):
            self.stock_type = TYPE_LIST[i]
            self.stock_type_name = TYPE_NAME_LIST[i]
            ret = self.update_process()
            if ret != RET_OK:
                self.stopped = True
                return ret
            self.callback()
        if self.havetimeout == True:
            self.status_text = STR_UPDB_TIMEOUT
        else:
            self.status_text = STR_UPDB_ALL_OK
        self.stopped = True
        return RET_OK

    def stop(self):
        self.stopped = True
