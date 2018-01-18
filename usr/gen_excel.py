##
## Function: Generate Excel File according to cycle and number specified by the user
## Input: Cycle, Number
## Output: T/F
from db.db_agency import *
import pandas as pd
import threading
import os

ERR_GEN_BASE = 20000
ERR_GEN_EXCE_ARGS = ERR_GEN_BASE + 1
ERR_GEN_EXCE_NO_BUSY_DAY = ERR_GEN_BASE + 2
ERR_GEN_CONS_TABLE = ERR_GEN_BASE + 3
ERR_GEN_FILL_VOLPER = ERR_GEN_BASE + 4
ERR_GEN_SAVE_EXCEL = ERR_GEN_BASE + 5
ERR_GEN_DB_RECOVERED = ERR_GEN_BASE + 6
RET_OK = 0

TYPE_SH = "Hu"
TYPE_HK = "Gang"
TYPE_SZ = "Shen"



ENGLISH = 1
CHINESE = 2

language = CHINESE

if language == ENGLISH:
    STATUS_IDLE = "GEN: Idle"
    STATUS_ERR = "GEN: Error.."
    STATUS_Done = "GEN: OK"
    STATUS_PREP_DATA = "GEN: Preparing..."
    STATUS_FIND_DATA = "GEN: Finding..."
    STATUS_GEN_EXCEL = "GEN: Generating Excel..."
    STATUS_DB_RECOVERED = "GEN: DB Recovered. PLS Update"
if language == CHINESE:
    STATUS_IDLE = "生成器：空闲"
    STATUS_ERR = "生成器：错误 代码 "
    STATUS_Done = "生成器：完成"
    STATUS_PREP_DATA = "生成器：准备中..."
    STATUS_FIND_DATA = "生成器：寻找数据..."
    STATUS_GEN_EXCEL = "生成器：生成 Excel..."
    STATUS_DB_RECOVERED = "生成器：数据库从灾难中恢复，请更新数据"


class gen_excel(threading.Thread):
    def __init__(self, mkt_type, cycle, num, callback):
        super(gen_excel, self).__init__()
        self.cycle = cycle
        self.num = num
        self.mkt_type = mkt_type
        self.gen_status = STATUS_IDLE
        self.stopped = False
        self.callback = callback

    def validate_args(self):
        try:
            self.cycle = int(self.cycle)
            self.num = int(self.num)
        except:
            return ERR_GEN_EXCE_ARGS

        if self.cycle < 1 or self.num < 1:
            return ERR_GEN_EXCE_ARGS

        if self.mkt_type not in [TYPE_HK, TYPE_SH, TYPE_SZ]:
            return ERR_GEN_EXCE_ARGS

        return RET_OK

    def init_db(self):
        self.db_agen = db_agency(self.mkt_type)

        ret = self.db_agen.init_db_tl()
        if ret != RET_OK:
            return ret

        ret = self.db_agen.check_db_normal()
        if ret != RET_OK:
            ret_ = self.db_agen.recover_db()
            if ret_ != RET_OK:
                return ret_
            return ERR_GEN_DB_RECOVERED


        return RET_OK

    def __get_all_busy_days(self):
        ret, list = self.db_agen.get_all_busy_days()
        if ret != RET_OK:
            return ret, []

        return RET_OK, list

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
            codes_dup.append([code_list[i][0], code_list[i][1], cnt])
            cnt += 1

        self.stock_codes_dup = codes_dup
        return RET_OK


    def gen_days(self):
        ## Get All Busy Day List
        ret, day_list = self.__get_all_busy_days()
        if ret != RET_OK:
            return ret

        ## Select Days
        days = []
        cnt = 0
        for d_index in range(len(day_list) - 1, -1 , (-1) * self.cycle):
            days.append(day_list[d_index])
            cnt += 1
            if cnt == self.num:
                break

        if len(days) == 0:
            return ERR_GEN_EXCE_NO_BUSY_DAY

        ## Make it in Order and Mark order
        days_reverse = []
        cnt = 0
        for i in range(len(days) - 1, -1, -1):
            days_reverse.append([days[i], cnt])
            cnt += 1

        self.days_dup = days_reverse

        return RET_OK

    ### Prepare days, stock codes
    def prep_data(self):
        self.gen_status = STATUS_PREP_DATA
        ret = self.validate_args()
        if ret != RET_OK:
            return ret

        ret = self.init_db()
        if ret != RET_OK:
            return ret


        ret = self.gen_codes()
        if ret != RET_OK:
            return ret

        ret = self.gen_days()
        if ret != RET_OK:
            return ret
        return RET_OK

    def __gen_columns(self):
        cols = []
        cols.append("Code")
        cols.append("Name")
        for day in self.days_dup:
            cols.append(str(day[0]) + "_" + "Volume")
            cols.append(str(day[0]) + "_" + "Percent")

        return RET_OK, cols

    def __init_table(self):
        data = []
        for code_dup in self.stock_codes_dup:
            data.append({
                "Code":code_dup[0],
                "Name":code_dup[1]
            })
        try:
            self.table = pd.DataFrame(data, columns=["Code","Name"])
        except:
            return ERR_GEN_CONS_TABLE

        for day_dup in self.days_dup:
            col_name_vol = str(day_dup[0]) + "_" + "volume"
            col_name_per = str(day_dup[0]) + "_" + "percent"
            try:
                self.table[col_name_vol] = 0
                self.table[col_name_per] = 0
            except:
                return ERR_GEN_CONS_TABLE
        return RET_OK

    def __fill_vol(self, code_dup, day_dup, vol, per):
        try:
            self.table.iloc[code_dup[2], 3 + day_dup[1] * 2 - 1] = vol
            self.table.iloc[code_dup[2], 3 + day_dup[1] * 2] = per
        except:
            return ERR_GEN_FILL_VOLPER
        return RET_OK


    def construct_table(self):
        ret = self.__init_table()
        if ret != RET_OK:
            return ret

        for day_dup in self.days_dup:

            for code_dup in self.stock_codes_dup:
                if self.stopped == True:
                    return -1
                self.gen_status = STATUS_FIND_DATA + " " + str(day_dup[0]) + " " + str(code_dup[1]) + " " + str(code_dup[0])
                ## Get vals
                ret, vals = self.db_agen.get_vol(code_dup[0], day_dup[0])
                if ret == RET_OK:
                    vol = vals[0]
                    per = vals[1]
                elif ret == ERR_DBAGEN_NO_VOL_FOUND:
                    vol = 0
                    per = 0
                else:
                    continue

                ## Fill in the table
                ret = self.__fill_vol(code_dup, day_dup, vol, per)
                if ret != RET_OK:
                    return ret

        return RET_OK

    def gen_excel(self):
        self.gen_status = STATUS_GEN_EXCEL
        file_name = "hkexnews_" + str(self.mkt_type) + ".xlsx"
        if os.path.exists(file_name):
            os.remove(file_name)
        try:
            writer = pd.ExcelWriter(file_name)
            self.table.to_excel(writer, 'page_1')
            writer.save()
        except:
            return ERR_GEN_SAVE_EXCEL
        self.gen_status = STATUS_Done
        return RET_OK

    def run(self):
        self.stopped = False
        ret = self.prep_data()
        if ret != RET_OK and ret != ERR_GEN_DB_RECOVERED:
            self.gen_status = STATUS_ERR + " " + str(ret)
            self.stopped = True
            return ret

        if ret == ERR_GEN_DB_RECOVERED:
            self.gen_status = STATUS_DB_RECOVERED
            self.stopped = True
            return ret

        ret = self.construct_table()
        if ret != RET_OK:
            self.gen_status = STATUS_ERR + " " + str(ret)
            self.stopped = True
            return ret

        ret = self.gen_excel()
        if ret != RET_OK:
            self.gen_status = STATUS_ERR + " " + str(ret)
            self.stopped = True
            return ret

        self.gen_status = STATUS_Done

        self.callback()
        self.stopped = True
        return RET_OK

    def get_gen_status(self):
        return self.gen_status

    def stop(self):
        self.stopped = True
