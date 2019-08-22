#
# Function:
#     Use either Selenuim or Request to grap html source and parse the stock info
# Main Methods:
#     Verify Arg
#         This is to verify the specified
#             1. stock type
#             2. specified date
#             3. method to get html
#     Get Html
#         Get Html Source via a method
#     Find Date
#         Find the date in src
#     Verify Date
#         verify if date equals to the one we defined
#     Find Table
#         Find stock information
# Author:
#     Zhen Zhang
# Date:
#     12/01/2018
# EMail:
#     zhangzhentctc@163.com


import requests
from crawls.methods.src_selenium import *
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from general.date_structure import *

import time

TYPE_SH = "Hu"
TYPE_HK = "Gang"
TYPE_SZ = "Shen"
TYPE_LIST = [TYPE_SH, TYPE_HK, TYPE_SZ]

LINK_SH = 'http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh'
LINK_HK = 'http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=hk'
LINK_SZ = 'http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sz'

CRAWL_METHOD_REQUEST = 1
CRAWL_METHOD_SELENIUM = 2
CRAWL_METHOD_LIST = [CRAWL_METHOD_REQUEST, CRAWL_METHOD_SELENIUM]

TIMEOUT = 10
XML_PARSER = "html.parser"

ERR_CRAWL_BASE = 1000
ERR_CRAWL_TYPE = ERR_CRAWL_BASE + 1
ERR_CRAWL_REQ_TIMEOUT = ERR_CRAWL_BASE + 2
ERR_CRAWL_INIT_SOUP = ERR_CRAWL_BASE + 3
ERR_CRAWL_SELE_GET_LINK = ERR_CRAWL_BASE + 12
ERR_CRAWL_DATE_FIND = ERR_CRAWL_BASE + 4
ERR_CRAWL_DATE_FORMAT = ERR_CRAWL_BASE + 5

ERR_CRAWL_STOCK_TL_FIND = ERR_CRAWL_BASE + 6
ERR_CRAWL_STOCK_TL_ERR = ERR_CRAWL_BASE + 7
ERR_CRAWL_STOCK_CODE = ERR_CRAWL_BASE + 8
ERR_CRAWL_STOCK_NAME = ERR_CRAWL_BASE + 9
ERR_CRAWL_STOCK_VOL = ERR_CRAWL_BASE + 10
ERR_CRAWL_STOCK_PER = ERR_CRAWL_BASE + 11

ERR_CRAWL_DATE_MATCH = ERR_CRAWL_BASE + 13

ERR_CRAWL_ARG = ERR_CRAWL_BASE + 14
ERR_CRAWL_RCVDATE_CON = ERR_CRAWL_BASE + 15

RET_OK = 0
RET_ERR = -1

class crawl:
    def __init__(self, req_date, type = TYPE_SH, method = CRAWL_METHOD_SELENIUM):
        self.type = type
        self.method = method
        self.req_date = req_date

    def crawl_validate_args(self):
        if self.type not in TYPE_LIST:
            return ERR_CRAWL_TYPE
        if self.type == TYPE_SH:
            self.link = LINK_SH
        if self.type == TYPE_HK:
            self.link = LINK_HK
        if self.type == TYPE_SZ:
            self.link = LINK_SZ

        if self.method not in CRAWL_METHOD_LIST:
            return ERR_CRAWL_TYPE

        self.req_struct_date = date_structure(self.req_date)
        ret = self.req_struct_date.parse_date()
        if ret == False:
            return ERR_CRAWL_ARG
        return RET_OK



    def crawl_get_info(self):
        if self.method == CRAWL_METHOD_REQUEST:
            try:
                self.resp = requests.get(self.link, timeout=TIMEOUT)
            except:
                self.crawl_report_err(ERR_CRAWL_REQ_TIMEOUT)
                return ERR_CRAWL_REQ_TIMEOUT
            pg_src = self.resp.text

        if self.method == CRAWL_METHOD_SELENIUM:
            sel = src_selenium(self.req_struct_date, self.link)
            ret = sel.sele_process()
            if ret != RET_OK:
                self.crawl_report_err(ERR_CRAWL_SELE_GET_LINK)
                return ret
            pg_src = sel.pg_src

        try:
            self.soup = BeautifulSoup(pg_src, XML_PARSER)
        except:
            self.crawl_report_err(ERR_CRAWL_INIT_SOUP)
            return ERR_CRAWL_INIT_SOUP
        return RET_OK


    def crawl_find_date(self):
        tag_pnlResult = self.soup.find("input", {"name": "txtShareholdingDate"})
        if tag_pnlResult == None:
            self.crawl_report_err(ERR_CRAWL_DATE_FIND)
            return ERR_CRAWL_DATE_FIND
        else:
            tag_date = tag_pnlResult["value"]
            if tag_date == None:
                self.crawl_report_err(ERR_CRAWL_DATE_FIND)
                return ERR_CRAWL_DATE_FIND
            else:
                print(tag_date)
                date = tag_date
                if self.__validate_date(date) == False:
                    self.crawl_report_err(ERR_CRAWL_DATE_FORMAT)
                    return ERR_CRAWL_DATE_FIND
                else:
                    self.rcv_date = date

        self.req_struct_rcv_date = date_structure(self.rcv_date)
        ret = self.req_struct_rcv_date.parse_date()
        if ret == False:
            return ERR_CRAWL_RCVDATE_CON

        return RET_OK

    def __validate_date(self, date_str):
        date_list = date_str.split("/")
        if len(date_list) == 3:
            return True
        else:
            return False

    def crawl_find_stock_tl(self):

        tables = self.soup.find_all("tbody")
        table = tables[1].find_all("tr")
        data = []
        for row in table:
            items = row.find_all("div")
            pure_items = []
            for item in items:
                pure_items.append(item.string)
            print(pure_items[1])
            print(pure_items[5])
            print(pure_items[7])

            ret, code = self.__parse_stock_code(pure_items[1])
            if ret == RET_ERR:
                self.crawl_report_err(ERR_CRAWL_STOCK_CODE)
                return ERR_CRAWL_STOCK_CODE

            ret, vol = self.__parse_stock_vol(pure_items[5])
            if ret == RET_ERR:
                self.crawl_report_err(ERR_CRAWL_STOCK_VOL)
                return ERR_CRAWL_STOCK_VOL

            ret, per = self.__parse_stock_per(pure_items[7])
            if ret == RET_ERR:
                print(per)
                self.crawl_report_err(ERR_CRAWL_STOCK_PER)
                return ERR_CRAWL_STOCK_PER

            data.append({
                "Code": code,
                "Name": pure_items[3],
                "Volume": vol,
                "Percent": per
            })
        self.stock_tl = pd.DataFrame(data, columns=["Code", "Name", "Volume", "Percent"])
        return RET_OK


    def __parse_stock_code(self, stock_code_str):
        try:
            stock_code = int(stock_code_str)
        except:
            return RET_ERR, -1
        return RET_OK, stock_code


    def __parse_stock_vol(self, stock_vol_str):
        if stock_vol_str == "":
            return RET_OK, 0
        try:
            stock_vol = int(stock_vol_str.replace(",", ""))
        except:
            return RET_ERR, -1
        if stock_vol >= 0:
            return RET_OK, stock_vol
        else:
            return RET_ERR, -1


    def __parse_stock_per(self, stock_per_str):
        if stock_per_str == "":
            return RET_OK, 0
        try:
            stock_per = float(stock_per_str.strip("%")) / 100
        except:
            return RET_OK, 0
        if stock_per >= 0 and stock_per <= 1:
            return RET_OK, stock_per
        else:
            return RET_OK, 0

    def crawl_report_err(self,err_type):
        print("Error")

    def crawl_process(self):
        ret = self.crawl_validate_args()
        if ret != RET_OK:
            return ret

        ret = self.crawl_get_info()
        if ret != RET_OK:
            return ret

        ret = self.crawl_find_date()
        if ret != RET_OK:
            return ret

        ret = self.verify_date()
        if ret != RET_OK:
            return ret

        ret = self.crawl_find_stock_tl()
        if ret != RET_OK:
            return ret

        return RET_OK

    def verify_date(self):
        ret = self.req_struct_date.compare_date(self.req_struct_rcv_date)
        if ret != True:
            return ERR_CRAWL_DATE_MATCH

        ret, week = self.req_struct_date.get_week()
        if ret == True and week == 5:
            return ERR_CRAWL_DATE_MATCH
        return RET_OK


    def crawl_print_ret(self):
        print(self.rcv_date)
        print(self.stock_tl)
