##
## Function: Generate Excel File according to cycle and number specified by the user
## Input: Cycle, Number
## Output: T/F
from db.db_agency import *
import pandas as pd
import threading

ERR_GEN_EXCE_ARGS = 1
ERR_GEN_EXCE_NO_BUSY_DAY = 2
ERR_GEN_CONS_TABLE = 3
ERR_GEN_FILL_VOLPER = 4
ERR_GEN_SAVE_EXCEL = 5
RET_OK = 0

TYPE_SH = "Hu"
TYPE_HK = "Gang"

STATUS_IDLE = "GEN: Idle"
STATUS_ERR = "GEN: Error.."
STATUS_Done = "GEN: OK"
STATUS_PREP_DATA = "GEN: Preparing..."
STATUS_FIND_DATA = "GEN: Finding..."
STATUS_GEN_EXCEL = "GEN: Generating Excel..."


class gen_excel(threading.Thread):
    def __init__(self, mkt_type, cycle, num):
        super(gen_excel, self).__init__()
        self.cycle = cycle
        self.num = num
        self.mkt_type = mkt_type
        self.gen_status = STATUS_IDLE

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
        try:
            writer = pd.ExcelWriter("Save_Excel_" + str(self.mkt_type) + ".xlsx")
            self.table.to_excel(writer, 'page_1')
            writer.save()
        except:
            return ERR_GEN_SAVE_EXCEL
        return RET_OK

    def run(self):
        ret = self.prep_data()
        if ret != RET_OK:
            self.gen_status = STATUS_ERR + " " + str(ret)
            return ret

        ret = self.construct_table()
        if ret != RET_OK:
            self.gen_status = STATUS_ERR + " " + str(ret)
            return ret

        ret = self.gen_excel()
        if ret != RET_OK:
            self.gen_status = STATUS_ERR + " " + str(ret)
            return ret

        self.gen_status = STATUS_Done
        return RET_OK

    def get_gen_status(self):
        return self.gen_status

