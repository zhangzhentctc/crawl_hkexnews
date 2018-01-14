##
## Function: Generate Excel File according to cycle and number specified by the user
## Input: Cycle, Number
## Output: T/F
from db.db_agency import *


ERR_GEN_EXCE_ARGS = 1
ERR_GEN_EXCE_NO_BUSY_DAY = 2


RET_OK = 0

TYPE_SH = "Hu"
TYPE_HK = "Gang"



class gen_excel:
    def __init__(self, mkt_type, cycle, num):
        self.cycle = cycle
        self.num = num
        self.mkt_type = mkt_type

    def validate_args(self):
        try:
            self.cycle = int(self.cycle)
            self.num = int(self.num)
        except:
            return ERR_GEN_EXCE_ARGS

        if self.cycle < 1 or self.num < 1:
            return ERR_GEN_EXCE_ARGS

        if self.mkt_type not in [TYPE_HK, TYPE_SH]:
            return ERR_GEN_EXCE_ARGS

        return RET_OK

    def init_db(self):
        self.db_agen = db_agency(self.mkt_type)
        ret = self.db_agen.init_db_tl()
        if ret != RET_OK:
            return ret
        return RET_OK

    def get_all_busy_days(self):
        ret, list = self.db_agen.get_all_busy_days()
        if ret != RET_OK:
            return ret

        self.busy_days = list
        return RET_OK

    def __get_all_stock_codes(self):
        ret, list = self.db_agen.get_all_stock_codes()
        if ret != RET_OK:
            return ret, []

        return RET_OK, list

    def gen_codes(self):
        ret, code_list = self.__get_all_stock_codes()
        if ret != RET_OK:
            return ret
        codes_dup = []
        cnt = 0
        for i in range(0, len(code_list)):
            codes_dup.append([code_list[i], cnt])
            cnt += 1

        self.stock_codes_dup = codes_dup
        return RET_OK


    def gen_days(self):
        days = []
        cnt = 0
        for d_index in range(len(self.busy_days) - 1, -1 , (-1) * self.cycle):
            days.append(self.busy_days[d_index])
            cnt += 1
            if cnt == self.num:
                break

        if len(days) == 0:
            return ERR_GEN_EXCE_NO_BUSY_DAY

        days_reverse = []
        cnt = 0
        for i in range(len(days) - 1, -1, -1):
            days_reverse.append([days[i], cnt])
            cnt += 1

        self.days = days_reverse

        return RET_OK

    ### Prepare days, stock codes
    def prep(self):
        ret = self.validate_args()
        if ret != RET_OK:
            return ret

        ret = self.get_all_stock_codes()
        if ret != RET_OK:
            return ret

        ret = self.get_all_busy_days()
        if ret != RET_OK:
            return ret

        ret = self.gen_days()
        if ret != RET_OK:
            return ret

    def __gen_columns(self):
        cols = []
        cols.append("Code")
        cols.append("Name")
        for day in self.days:
            cols.append(str(day) + "_" + "Volume")
            cols.append(str(day) + "_" + "Percent")

        return RET_OK, cols

    def construct_table(self):
        ret, columns = self.__gen_columns()
        if ret != RET_OK:
            return ret

        data = []
        for day_dup in self.days_dup:
            for code_dup in self.stock_codes_dup:
                ## Get vals
                ret, vals = self.db_agen.get_vol(code, day)
                if ret == RET_OK:
                    vol = vals[0]
                    per = vals[1]
                elif ret == ERR_DBAGEN_NO_VOL_FOUND:
                    vol = 0
                    per = 0
                else:
                    continue

                ## Fill in the table
                data.append({

                })








