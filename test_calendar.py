import calendar
import datetime
import os

today = datetime.date.today()
theyear = today.year
themonth = today.month

html_c = calendar.HTMLCalendar()

# 保存するフォルダ/カレンダーのファイル名.htmlで記入↓
path = ""

with open(path, mode='w') as f:
    f.write(html_c.formatmonth(theyear, themonth, withyear=True))
