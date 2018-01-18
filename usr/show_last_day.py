import threading
from db.db_agency import *


class show_last_day(threading.Thread):
    def __init__(self):
        super(show_last_day, self).__init__()
        self.last_day_sh = ""
        self.last_day_hk = ""
        self.last_day_sz = ""


    def get_last_day(self, mkt_type):
        self.db_agen = db_agency(mkt_type)
        ret = self.db_agen.init_db_tl()
        if ret != RET_OK:
            return ret, ""

        ret, last_day = self.db_agen.get_last_busy_day()
        if ret != RET_OK:
            return ret, ""
        return RET_OK,  last_day

    def process(self):
        ret, last_day_sh = self.get_last_day(TYPE_SH)
        if ret != RET_OK:
            return ret
        self.last_day_sh = last_day_sh

        ret, last_day_hk = self.get_last_day(TYPE_HK)
        if ret != RET_OK:
            return ret
        self.last_day_hk = last_day_hk

        ret, last_day_sz = self.get_last_day(TYPE_SZ)
        if ret != RET_OK:
            return ret
        self.last_day_sz = last_day_sz
        return RET_OK

