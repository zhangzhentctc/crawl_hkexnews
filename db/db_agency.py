#
# Function:
#     Store day, month, year in both int and string
# Methods:
#     Get Hungary Dates
#         Func: Get all hungary days in a list
#         Input: today
#         Output: List
#     Store Day data:
#         Func: Store data of a day to db
#         Input: DataTable, Day
#         Output: T/F
#     Mark Free Day:
#         Func: Mark a specified day to Free
#         Input: Day
#         Output: T/F
#     Get Day Data:
#         Func: Get data of a day from db
#         Input: Day
#         Output: Ret, DataTable
# Author:
#     Zhen Zhang
# Date:
#     12/01/2018
# EMail:
#     zhangzhentctc@163.com

from db.dbop.db_op import *
import datetime

START_DATE = "2017-03-17"

DBAGEN_QUERY_DAY_STATUS_ = "select mark from stock_day where day = "
DBAGEN_QUERY_LAST_DAY = "select max(day) from stock_day"
DBAGEN_QUERY_BUSY_DAYS = "select day from stock_day where mark = 1"
DBAGEN_QUERY_STOCK_DODES_NAMES = "select code,name from stock_info"
DBAGEN_QUERY_CODE_ = "select * from stock_info where code = "
DBAGEN_QUERY_HUNGRY_DAY = "select * from stock_day where mark = 0"
DBAGEN_CHECK_EMPTY_SQL = "SELECT name FROM sqlite_master WHERE type='table'"
DBAGEN_CREATE_TL_DAY_SQL = "create table stock_day(" \
                           "day date primary key not null," \
                           "mark int" \
                           ")"
DBAGEN_CREATE_TL_INFO_SQL = "create table stock_info(" \
                            "code int primary key not null," \
                            "name varchar(50)" \
                            ")"
DBAGEN_CREATE_TL_VOL_SQL = "create table stock_vol(" \
                           "id integer primary key autoincrement," \
                           "code int not null," \
                           "day date not null," \
                           "volume int," \
                           "percent real" \
                           ")"
ERR_DBAGEN_NOT_EMPTY = 1
ERR_DBAGEN_DAY_TOUCHED = 2
ERR_DBAGEN_MAX_DAY = 3
ERR_DBAGEN_NO_BUSY_DAY = 4
ERR_DBAGEN_NO_STORED_CODE = 5
ERR_DBAGEN_NO_VOL_FOUND = 6

RET_OK = 0

class db_agency:
    def __init__(self, type):
        self.dbop = db_op(type)

    def db_conn_cur(self):
        ret = self.dbop.db_connect()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_open_cur()
        if ret != RET_OK:
            return ret
        return RET_OK

    def db_conn_cur_close(self):
        ret = self.dbop.db_close_cur()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_disconnect()
        if ret != RET_OK:
            return ret
        return RET_OK

    def get_hungry_days(self):
        days_list = []
        ret, values = self.__exec_single_query(DBAGEN_QUERY_HUNGRY_DAY)
        if ret != RET_OK:
            return ret, days_list
        for raw in values:
            days_list.append(raw[0])
        return RET_OK, days_list

    def get_all_busy_days(self):
        busy_days = []
        ret, values = self.__exec_single_query(DBAGEN_QUERY_BUSY_DAYS)
        if ret != RET_OK:
            return ret, busy_days
        if len(values) == 0:
            return ERR_DBAGEN_NO_BUSY_DAY,busy_days

        for raw in values:
            busy_days.append(str(raw[0]))
        return RET_OK, busy_days

    def get_all_stock_codes(self):
        codes = []
        ret, values = self.__exec_single_query(DBAGEN_QUERY_STOCK_DODES_NAMES)
        if ret != RET_OK:
            return ret, codes
        if len(values) == 0:
            return ERR_DBAGEN_NO_STORED_CODE,codes

        for raw in values:
            codes.append([str(raw[0]),str(raw[1])])
        return RET_OK, codes

    ### OPEN DB FIRST!!!
    def get_vol(self, code, date):
        # codes = []
        # select volume, percent from stock_vol where code = ? and day = ?
        sql = "select volume, percent from stock_vol where code = " + \
            "'" + str(code) + "'" + " and day = " + \
            "'" + str(date) + "'"
        ret, values = self.__exec_single_query(sql)
        if ret != RET_OK:
            return ret, []
        if len(values) == 0:
            return ERR_DBAGEN_NO_VOL_FOUND, []

        return RET_OK, values[0]



    def mark_day_rest(self, day):
        ret = self.dbop.db_connect()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_open_cur()
        if ret != RET_OK:
            return ret

        sql = "update stock_day set mark = 8 where day = " + "'" + str(day) + "'"
        ret = self.dbop.db_exec_sql(sql)
        if ret != RET_OK:
            return ret

        ## Done
        ret = self.dbop.db_commit()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_close_cur()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_disconnect()
        if ret != RET_OK:
            return ret

        return RET_OK


    def store_day_data(self, day, data):
        ret = self.dbop.db_connect()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_open_cur()
        if ret != RET_OK:
            return ret

        # Lookup Day Status
        sql = DBAGEN_QUERY_DAY_STATUS_ + "'"+ day + "'"
        ret = self.dbop.db_exec_sql(sql)
        if ret != RET_OK:
            return ret

        ret, values = self.dbop.db_fetall()
        if ret != RET_OK:
            return ret

        if str(values[0][0]) != "0":
            return ERR_DBAGEN_DAY_TOUCHED

        # Stock lines
        for pos in range(0, len(data.index)):
            code = data["Code"][pos]
            name = data["Name"][pos]
            name = self.name_process(name)
            vol = data["Volume"][pos]
            per = data["Percent"][pos]
            ### Check Stock Code Info
            ret = self.dbop.db_exec_sql(DBAGEN_QUERY_CODE_ + str(code))
            if ret != RET_OK:
                return ret

            ret, values = self.dbop.db_fetall()
            if ret != RET_OK:
                return ret
            if len(values) == 0:
                sql = "insert into stock_info(code, name) values (" + \
                      "'" + str(code) + "'" + "," + \
                      "'" + str(name) + "'" + \
                      ")"
                ret = self.dbop.db_exec_sql(sql)
                if ret != RET_OK:
                    return ret
            # Insert Stock Vol
            sql = "insert into stock_vol(code, day, volume, percent) values (" + \
                  "'" + str(code) + "'" + "," + \
                  "'" + str(day) + "'" + "," + \
                  "'" + str(vol) +  "'" + "," + \
                  "'" + str(per) +  "'" + \
                  ")"

            ret = self.dbop.db_exec_sql(sql)
            if ret != RET_OK:
                return ret

        ## Update Day Status
        sql = "update stock_day set mark = 1 where day = " + "'" + str(day) + "'"
        ret = self.dbop.db_exec_sql(sql)
        if ret != RET_OK:
            return ret

        ## Done
        ret = self.dbop.db_commit()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_close_cur()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_disconnect()
        if ret != RET_OK:
            return ret

        return RET_OK

    def name_process(self, name):
        str = name.split("'")
        if len(str) == 1:
            return name
        else:
            str = name.replace("'",",")
            return str

    def init_db_tl(self):
        ret = self.__check_db_empty()

        if ret != ERR_DBAGEN_NOT_EMPTY and ret != RET_OK:
            return ret

        # If Empty, create
        if ret == RET_OK:
            ret = self.__create_tl_day()
            if ret != RET_OK:
                return ret

            ret = self.__fill_tl_days()
            if ret != RET_OK:
                return ret
        else:
            ret = self.__fill_recent_days()
            if ret != RET_OK:
                return ret

        return RET_OK

    def __fill_recent_days(self):
        ret, values = self.__exec_single_query(DBAGEN_QUERY_LAST_DAY)
        if ret != RET_OK:
            return ret

        if len(values) == 0:
            return ERR_DBAGEN_MAX_DAY
        last_day_str = str(values[0][0])
        last_day = datetime.datetime.strptime(last_day_str, '%Y-%m-%d')
        today_str = str(datetime.date.today())
        today = datetime.datetime.strptime(today_str, '%Y-%m-%d')
        day_gap = today - last_day

        ## If Gap Day is over 1
        if day_gap.days > 1:
            date_list = self.__gen_dateRange(last_day_str, today)
            # Delete 1st one
            date_list.pop(0)

            ret = self.dbop.db_connect()
            if ret != RET_OK:
                return ret

            ret = self.dbop.db_open_cur()
            if ret != RET_OK:
                return ret

            for day in date_list:
                sql = "insert into stock_day(day, mark) values (" + \
                      "'" + str(day) + "'" + "," + \
                      "'" + "0" + "'" + \
                      ")"
                ret = self.dbop.db_exec_sql(sql)
                if ret != RET_OK:
                    return ret

            ret = self.dbop.db_commit()
            if ret != RET_OK:
                return ret

            ret = self.dbop.db_close_cur()
            if ret != RET_OK:
                return ret

            ret = self.dbop.db_disconnect()
            if ret != RET_OK:
                return ret

            return RET_OK
        else:
            return RET_OK




    def __fill_tl_days(self):
        ## Get Day List from XX to yesterday
        today = str(datetime.date.today())
        date_list = self.__gen_dateRange(START_DATE, today)

        ret = self.dbop.db_connect()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_open_cur()
        if ret != RET_OK:
            return ret

        for day in date_list:
            sql = "insert into stock_day(day, mark) values (" + \
                "'" + str(day) + "'" + "," + \
                "'" + "0" + "'" + \
                ")"
            ret = self.dbop.db_exec_sql(sql)
            if ret != RET_OK:
                return ret

        ret = self.dbop.db_commit()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_close_cur()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_disconnect()
        if ret != RET_OK:
            return ret

        return RET_OK


    def __gen_dateRange(self, start, end, step=1, format="%Y-%m-%d"):
        strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
        days = (strptime(end, format) - strptime(start, format)).days
        return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]

    def __exec_pure_query(self, sql):
        ret = self.dbop.db_exec_sql(sql)
        if ret != RET_OK:
            return ret,[]

        ret, values = self.dbop.db_fetall()
        if ret != RET_OK:
            return ret,[]
        return RET_OK, values


    def __exec_single_query(self, sql):
        ret = self.dbop.db_connect()
        if ret != RET_OK:
            return ret,[]

        ret = self.dbop.db_open_cur()
        if ret != RET_OK:
            return ret,[]

        ret = self.dbop.db_exec_sql(sql)
        if ret != RET_OK:
            return ret,[]

        ret, values = self.dbop.db_fetall()
        if ret != RET_OK:
            return ret,[]

        ret = self.dbop.db_close_cur()
        if ret != RET_OK:
            return ret,[]

        ret = self.dbop.db_disconnect()
        if ret != RET_OK:
            return ret,[]

        return RET_OK, values


    def __check_db_empty(self):
        ret, values = self.__exec_single_query(DBAGEN_CHECK_EMPTY_SQL)
        if ret != RET_OK:
            return ret

        if len(values) != 0:
            return ERR_DBAGEN_NOT_EMPTY

        return RET_OK

    def __create_tl_day(self):
        ret = self.dbop.db_connect()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_open_cur()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_exec_sql(DBAGEN_CREATE_TL_DAY_SQL)
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_exec_sql(DBAGEN_CREATE_TL_INFO_SQL)
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_exec_sql(DBAGEN_CREATE_TL_VOL_SQL)
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_close_cur()
        if ret != RET_OK:
            return ret

        ret = self.dbop.db_disconnect()
        if ret != RET_OK:
            return ret

        return RET_OK