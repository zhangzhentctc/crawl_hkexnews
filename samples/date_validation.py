import time

def is_valid(date):
    try:
        time.strptime(date, "%Y-%m-%d")
    except:
        return False
    return True

date = "2017-02-29"
ret = is_valid(date)
if ret != True:
    print("No")
else:
    print("Yes")