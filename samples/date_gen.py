import datetime

def dateRange(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]

def get_yesterday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday

if __name__ == '__main__':
    #print(get_yesterday())
    #today = str(datetime.date.today())
    #print(dateRange("2017-03-17", today))

    a = '2016-03-15'
    b = '2018-01-11'
    today_str = str(datetime.date.today())
    a_ = datetime.datetime.strptime(a, '%Y-%m-%d')
    b_ = datetime.datetime.strptime(b, '%Y-%m-%d')
    today = datetime.datetime.strptime(today_str, '%Y-%m-%d')
    c = today - b_
    print(c.days)
    #print(a_)
    print(b_)

    print(today)
    list = dateRange(b, today_str)
    list.pop(0)
    print(list)


    week = datetime.datetime.strptime(a, "%Y-%m-%d").weekday()
    print(str(week) + " " + a)
    if week == 1:
        print("1111")