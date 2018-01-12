from selenium import webdriver  #导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys  #导入Keys
from selenium.webdriver.support.ui import Select
import time

#driver = webdriver.Safari()
driver = webdriver.PhantomJS()  #指定使用的浏览器，初始化webdriver
driver.get("http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=hk")  #请求网页地址
#time.sleep(5)
#assert "Python" in driver.title  #看看Python关键字是否在网页title中，如果在则继续，如果不在，程序跳出。
select_day = Select(driver.find_element_by_name("ddlShareholdingDay"))  #找到name为q的元素，这里是个搜索框


select_month = Select(driver.find_element_by_name("ddlShareholdingMonth"))  #找到name为q的元素，这里是个搜索框


select_year = Select(driver.find_element_by_name("ddlShareholdingYear"))  #找到name为q的元素，这里是个搜索框
select_year.select_by_value("2017")
select_day.select_by_value("03")
select_month.select_by_value("12")
btnSearch = driver.find_element_by_name("btnSearch")
btnSearch.click()

pg_src = driver.page_source
print(pg_src)

driver.close()  #关闭webdriver