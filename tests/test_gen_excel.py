from usr.gen_excel import *
import time

times = time.time()
gen_e = gen_excel(TYPE_HK, 2, 3)
ret = gen_e.prep_data()
if ret != RET_OK:
    print(ret)
    exit(0)
timee = time.time()
print("Prep Done:" + str(timee - times))

times = time.time()
ret = gen_e.construct_table()
if ret != RET_OK:
    print(ret)
    exit(0)
timee = time.time()
print("Cons Done:" + str(timee - times))
gen_e.gen_excel()