##
## Function: Download data that we do not have from web
## Input:  data
## Output: None

from crawls.crawl import *
from db.db_agency import *
import threading

class update_db(threading.Thread):
    def __init__(self, type):
        super(update_db, self).__init__()
        self.status_text = "Idle"
        self.stock_type = type
        self.db_agen = db_agency(self.stock_type)

    def get_empty_days(self):
        self.status_text = "Get Empty Days"
        ret = self.db_agen.init_db_tl()
        if ret != RET_OK:
            return ret
        ret, list = self.db_agen.get_hungry_days()
        if ret != RET_OK:
            return ret

        self.empty_days = list
        return RET_OK

    def update_info(self):
        for day in self.empty_days:
            self.status_text = "crawl " + str(day)
            crawl_t = crawl(day, self.stock_type)
            ret = crawl_t.crawl_process()
            if ret == ERR_CRAWL_DATE_MATCH:
                ret = self.db_agen.mark_day_rest(day)
                if ret != RET_OK:
                    self.update_err(ret)
                    continue
            elif ret == RET_OK:
                self.status_text = "store " + str(day)
                ret = self.db_agen.store_day_data(day, crawl_t.stock_tl)
                if ret != RET_OK:
                    self.update_err(ret)
                    continue
            else:
                self.update_err(ret)
                continue

    def update_process(self):
        ret = self.get_empty_days()
        if ret != RET_OK:
            self.status_text = "crawl Error " + str(ret)
            return ret

        ret = self.update_info()
        if ret != RET_OK:
            self.status_text = "crawl Error " + str(ret)
            return ret
        self.status_text = "crawl OK"
        return RET_OK

    def get_update_status(self):
        return self.status_text

    def update_err(self, ret):
        print(ret)

    def run(self):
        ret = self.update_process()
        if ret != RET_OK:
            return ret
        return RET_OK