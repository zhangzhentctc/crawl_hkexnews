from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time


ERR_SELENIUM_BASE = 2000
ERR_SELENIUM_ARG = ERR_SELENIUM_BASE + 1
ERR_SELENIUM_DRIVER = ERR_SELENIUM_BASE + 2
ERR_SELENIUM_GET_TIMEOUT = ERR_SELENIUM_BASE + 3
ERR_SELENIUM_FIND_YEAR = ERR_SELENIUM_BASE + 4
ERR_SELENIUM_FIND_MONTH = ERR_SELENIUM_BASE + 5
ERR_SELENIUM_FIND_DAY = ERR_SELENIUM_BASE + 6
ERR_SELENIUM_FIND_BTN = ERR_SELENIUM_BASE + 7
ERR_SELENIUM_SET_YEAR = ERR_SELENIUM_BASE + 8
ERR_SELENIUM_SET_MONTH = ERR_SELENIUM_BASE + 9
ERR_SELENIUM_SET_DAY = ERR_SELENIUM_BASE + 10
ERR_SELENIUM_SET_BTN = ERR_SELENIUM_BASE + 11
ERR_SELENIUM_INTERNAL = ERR_SELENIUM_BASE + 12
ERR_SELENIUM_GET_SRC = ERR_SELENIUM_BASE + 13
ERR_SELENIUM_DRIVER_CLOSE = ERR_SELENIUM_BASE + 14
RET_ERR = -1
RET_OK = 0
TIMEOUT = 10


class src_selenium:
    def __init__(self, date_strcture):
        self.date_strcture = date_strcture
        #self.date_strcture.show()

    def selenium_err(self, err_type):
        print("Err")

    def init_driver(self):
        try:
            self.driver = webdriver.PhantomJS()
        except:
            self.selenium_err(ERR_SELENIUM_DRIVER)
            return ERR_SELENIUM_DRIVER
        return RET_OK


    def get_link(self):
        try:
            self.driver.get("http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=hk")
            self.driver.set_page_load_timeout(TIMEOUT)
        except:
            self.selenium_err(ERR_SELENIUM_GET_TIMEOUT)
            return ERR_SELENIUM_GET_TIMEOUT
        return RET_OK


    def set_date(self):
        try:
            select_day = Select(self.driver.find_element_by_name("ddlShareholdingDay"))
        except:
            self.selenium_err(ERR_SELENIUM_FIND_DAY)
            return ERR_SELENIUM_FIND_DAY

        try:
            select_month = Select(self.driver.find_element_by_name("ddlShareholdingMonth"))
        except:
            self.selenium_err(ERR_SELENIUM_FIND_MONTH)
            return ERR_SELENIUM_FIND_MONTH

        try:
            select_year = Select(self.driver.find_element_by_name("ddlShareholdingYear"))
        except:
            self.selenium_err(ERR_SELENIUM_FIND_YEAR)
            return ERR_SELENIUM_FIND_YEAR

        try:
            btnSearch = self.driver.find_element_by_name("btnSearch")
        except:
            self.selenium_err(ERR_SELENIUM_FIND_BTN)
            return ERR_SELENIUM_FIND_BTN


        try:
            select_day.select_by_value(self.date_strcture.date_day_str)
        except:
            self.selenium_err(ERR_SELENIUM_SET_DAY)
            return ERR_SELENIUM_SET_DAY

        try:
            select_month.select_by_value(self.date_strcture.date_month_str)
        except:
            self.selenium_err(ERR_SELENIUM_SET_MONTH)
            return ERR_SELENIUM_SET_MONTH

        try:
            select_year.select_by_value(self.date_strcture.date_year_str)
        except:
            self.selenium_err(ERR_SELENIUM_SET_YEAR)
            return ERR_SELENIUM_SET_YEAR

        try:
            btnSearch.click()
        except:
            self.selenium_err(ERR_SELENIUM_SET_BTN)
            return ERR_SELENIUM_SET_BTN

        return RET_OK

    def get_src(self):
        try:
            self.pg_src = self.driver.page_source
        except:
            self.selenium_err(ERR_SELENIUM_GET_SRC)
            return ERR_SELENIUM_GET_SRC

        return RET_OK

    def close_driver(self):
        try:
            self.driver.close()
            self.driver.quit()
        except:
            return ERR_SELENIUM_DRIVER_CLOSE
        return RET_OK

    def print_src(self):
        print(self.pg_src)

    def sele_process(self):
        ret = self.init_driver()
        if ret != RET_OK:
            return ret

        ret = self.get_link()
        if ret != RET_OK:
            return ret

        ret = self.set_date()
        if ret != RET_OK:
            return ret

        ret = self.get_src()
        if ret != RET_OK:
            return ret

        ret = self.close_driver()
        if ret != RET_OK:
            return ret

        return RET_OK
        #self.print_src()