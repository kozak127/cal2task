import urllib
import datetime
import calendar


def download_file(url, path):
    urllib.urlretrieve(url, path)


def getWeekNumbersInMonth(month, year):
    to_return = []

    days = xrange(1, calendar.monthrange(year, month)[1] + 1)
    for day in days:
        week = datetime.date(year, month, day).isocalendar()[1]
        if not (week in to_return):
            to_return.append(week)

    return to_return
