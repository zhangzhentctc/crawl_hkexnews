from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


ERR_SELENIUM_ARG = 1
ERR_SELENIUM_DRIVER = 2
ERR_SELENIUM_GET_TIMEOUT = 3
ERR_SELENIUM_FIND_YEAR = 4
ERR_SELENIUM_FIND_MONTH = 5
ERR_SELENIUM_FIND_DAY = 6
ERR_SELENIUM_FIND_BTN = 6
ERR_SELENIUM_SET_YEAR = 4
ERR_SELENIUM_SET_MONTH = 5
ERR_SELENIUM_SET_DAY = 6
ERR_SELENIUM_SET_BTN = 6
ERR_SELENIUM_INTERNAL = 7
ERR_SELENIUM_GET_SRC = 8
RET_ERR = -1
RET_OK = 0
TIMEOUT = 10


class src_selenium:
    def __init__(self, date):
        self.date = date

    def selenium_err(self, err_type):
        print("Err")

    ## Splite Date Str by Symbols
    def __split_date(self):
        date_list = []
        for symbol in ["/", "-", ".", ":"]:
            date_list = self.date.split(symbol)
            if len(date_list) == 3:
                break

        if len(date_list) != 3:
            return False,[]
        else:
            return True, date_list

    def __convert_date_list_int(self, date_list):
        for i in range(0, len(date_list)):
            try:
                date_list[i] = int(date_list[i])
            except:
                self.selenium_err(ERR_SELENIUM_ARG)
                return False
        return True

    def __parse_date(self, date_list):
        if date_list[0] > 999 and date_list[0] < 10000:
            self.date_year = date_list[0]
            self.date_month = date_list[1]
            self.date_day = date_list[2]
        elif date_list[2] > 999 and date_list[2] < 10000:
            self.date_year = date_list[2]
            self.date_month = date_list[1]
            self.date_day = date_list[0]
        else:
            self.selenium_err(ERR_SELENIUM_ARG)
            return False
        return True

    def __validate_date(self):
        if self.date_year < 2017:
            return False
        if self.date_month < 1 or self.date_month > 12:
            return False
        if self.date_day < 1 or self.date_day > 31:
            return False
        return True

    def verify_arg(self):
        ret, date_list = self.__split_date()
        if ret == False:
            self.selenium_err(ERR_SELENIUM_ARG)
            return False

        ret = self.__convert_date_list_int(date_list)
        if ret == False:
            self.selenium_err(ERR_SELENIUM_ARG)
            return False

        ret = self.__parse_date(date_list)
        if ret == False:
            self.selenium_err(ERR_SELENIUM_ARG)
            return False

        ret = self.__validate_date()
        if ret == False:
            self.selenium_err(ERR_SELENIUM_ARG)
            return False

    def prep_date(self):
        try:
            self.date_year_str = str(self.date_year)

            if self.date_month > 0 and self.date_month < 10:
                self.date_month_str = "0" + str(self.date_month)
            else:
                self.date_month_str = str(self.date_month)

            if self.date_day > 0 and self.date_day < 10:
                self.date_day_str = "0" + str(self.date_day)
            else:
                self.date_day_str = str(self.date_day)
        except:
            self.selenium_err(ERR_SELENIUM_INTERNAL)
            return False

        return True


    def init_driver(self):
        try:
            self.driver = webdriver.PhantomJS()
        except:
            self.selenium_err(ERR_SELENIUM_DRIVER)
            return False
        return True


    def get_link(self):
        try:
            self.driver.get("http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=hk")
            self.driver.set_page_load_timeout(TIMEOUT)
        except:
            self.selenium_err(ERR_SELENIUM_GET_TIMEOUT)
            return False
        return True


    def set_date(self):
        try:
            select_day = Select(self.driver.find_element_by_name("ddlShareholdingDay"))
        except:
            self.selenium_err(ERR_SELENIUM_FIND_DAY)
            return False

        try:
            select_month = Select(self.driver.find_element_by_name("ddlShareholdingMonth"))
        except:
            self.selenium_err(ERR_SELENIUM_FIND_DAY)
            return False

        try:
            select_year = Select(self.driver.find_element_by_name("ddlShareholdingYear"))
        except:
            self.selenium_err(ERR_SELENIUM_FIND_DAY)
            return False

        try:
            btnSearch = self.driver.find_element_by_name("btnSearch")
        except:
            self.selenium_err(ERR_SELENIUM_FIND_BTN)
            return False


        try:
            select_day.select_by_value(self.date_day_str)
        except:
            self.selenium_err(ERR_SELENIUM_SET_DAY)
            return False

        try:
            select_month.select_by_value(self.date_month_str)
        except:
            self.selenium_err(ERR_SELENIUM_SET_MONTH)
            return False

        try:
            select_year.select_by_value(self.date_year_str)
        except:
            self.selenium_err(ERR_SELENIUM_SET_YEAR)
            return False

        try:
            btnSearch.click()
        except:
            self.selenium_err(ERR_SELENIUM_SET_BTN)
            return False

        return True

    def get_src(self):
        try:
            self.pg_src = self.driver.page_source
        except:
            self.selenium_err(ERR_SELENIUM_GET_SRC)
            return False

        return True

    def print_src(self):
        print(self.pg_src)

    def sele_process(self):
        if self.verify_arg() == False:
            return False

        if self.prep_date() == False:
            return False


        if self.init_driver() == False:
            return False

        if self.get_link() == False:
            return False

        if self.set_date() == False:
            return False

        if self.get_src() == False:
            return False
        return True
        #self.print_src()