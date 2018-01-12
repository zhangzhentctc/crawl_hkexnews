from crawls.crawl import *


crawl_sh = crawl("2017-12-24")
ret = crawl_sh.crawl_process()
if ret != RET_OK:
    print(ret)
else:
    crawl_sh.crawl_print_ret()
