# a = {'name': 'hahha', 'sex': 1, 'aa': 2}
# print('name' and 'sex' and 'as' in a.keys())
import datetime

a = '2019-03-22 23:50:51'
b = '2019-03-22 23:51:51'

def getTimeFromStr(str):
    getdate = str.split()[0].split('-')
    gettime = str.split()[1].split(':')
    year = int(getdate[0])
    month = int(getdate[1])
    day = int(getdate[2])
    hour = int(gettime[0])
    min = int(gettime[1])
    sec = int(gettime[2])
    # datetime.datetime(2019, 3, 22, 23, 51, 51)
    # return year, month, day, hour, min, sec
    return datetime.datetime(year,month, day, hour, min, sec)

# x = datetime.datetime()
y = datetime.datetime(2019, 3, 22, 23, 51, 51)
print(getTimeFromStr(a))
