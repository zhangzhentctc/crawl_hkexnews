#
# Structure:
#     Store day, month, year in both int and string
# Methods:
#     Parse
#         Parse date in string to this structure
#     Compare
#         Compare two date_structure
# Author:
#     Zhen Zhang
# EMail:
#     zhangzhentctc@163.com

class date_structure:
    def __init__(self, date):
        self.date = date
        self.date_day = 0
        self.date_day_str = ""
        self.date_month = 0
        self.date_month_str = ""
        self.date_year = 0
        self.date_year_str = ""

    def parse_date(self):
        ret, date_list = self.__split_date()
        if ret == False:
            return False

        ret = self.__convert_date_list_int(date_list)
        if ret == False:
            return False

        ret = self.__parse_date(date_list)
        if ret == False:
            return False

        ret = self.__validate_date()
        if ret == False:
            return False

        ret = self.__gen_str_date()
        if ret == False:
            return False

        return True


    def compare_date(self, that_date):
        if self.date_day == that_date.date_day and \
            self.date_month == that_date.date_month and \
            self.date_year == that_date.date_year:
            return True
        else:
            return  False


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

    def __gen_str_date(self):
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
            return False

        return True
