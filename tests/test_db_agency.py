from crawls.crawl import *
from db.db_agency import *

#day = "2017-12-24"

db_agen = db_agency()
ret = db_agen.init_db_tl()
if ret != RET_OK:
    print(ret)
ret, list = db_agen.get_hungry_days()
if ret != RET_OK:
    print(ret)
else:
    print(list)

for day in list:
    crawl_sh = crawl(day)
    ret = crawl_sh.crawl_process()
    if ret == ERR_CRAWL_DATE_MATCH:
        ret = db_agen.mark_day_rest(day)
        if ret != RET_OK:
            print(ret)
    elif ret == RET_OK:
        ret = db_agen.store_day_data(day, crawl_sh.stock_tl)
        if ret != RET_OK:
            print(ret)
    else:
        print(ret)
    print(str(day) + ": Done")


