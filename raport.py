import calendar

import config
import misc


class Raport:

    def __init__(self, group):
        self.minutes = 0.0
        self.summary = ""
        self.group = group

    def populate(self, events):
        pass

    def to_plain_list(self, interval):
        return [str(self.get_duration(interval)), self.summary]

    def get_duration(self, interval):
        if interval == 'hours':
            return round(self.minutes / 60, 2)
        elif interval == 'minutes':
            return self.minutes
        else:
            return self.minutes

    def remove_trailing_summary_delimeter(self):
        self.summary = self.summary[:-2]

    def add_event(self, event):
        self.minutes = self.minutes + event.get_duration()
        self.summary = self.summary + event.summary + config.summary_delimeter


class DailyRaportForGroup(Raport):

    def __init__(self, group, day, events):
        self.group = group
        self.day = day
        self.minutes = 0.0
        self.summary = ""
        self.populate(events)

    def populate(self, events):
        for event in events:
            if (event.is_day_matching(self.day) and
                    event.is_group_matching(self.group)):
                self.add_event(event)
        self.remove_trailing_summary_delimeter()


class DailyRaportHelper:

    def create_raports(self, events, month, year):
        to_return = []
        days = xrange(1, calendar.monthrange(year, month)[1] + 1)
        for day in days:
            for group in config.group_dict:
                raport = DailyRaportForGroup(group, day, events)
                to_return.append(raport)
        return to_return

    def get_hours(self, day, raports):
        hours = 0.0
        for raport in self.get_raports(day, raports):
            hours = hours + raport.get_duration('hours')
        return hours

    def get_raports(self, day, raports):
        to_return = []
        for raport in raports:
            if raport.day == day:
                to_return.append(raport)
        return to_return


class WeeklyRaportForGroup(Raport):

    def __init__(self, group, week, events):
        self.group = group
        self.week = week
        self.minutes = 0.0
        self.summary = ""
        self.populate(events)

    def populate(self, events):
        for event in events:
            if (event.is_week_matching(self.week) and
                    event.is_group_matching(self.group)):
                self.add_event(event)
        self.remove_trailing_summary_delimeter()


class WeeklyRaportHelper:

    def create_raports(self, events, month, year):
        to_return = []

        weeks = misc.getWeekNumbersInMonth(month, year)
        for week in weeks:
            for group in config.group_dict:
                raport = WeeklyRaportForGroup(group, week, events)
                to_return.append(raport)
        return to_return

    def get_hours(self, week, raports):
        hours = 0.0
        for raport in self.get_raports(week, raports):
            hours = hours + raport.get_duration('hours')
        return hours

    def get_raports(self, week, raports):
        to_return = []
        for raport in raports:
            if raport.week == week:
                to_return.append(raport)
        return to_return


class MonthlyRaportForGroup(Raport):

    def __init__(self, group, month, events):
        self.group = group
        self.minutes = 0.0
        self.month = month
        self.summary = ""
        self.populate(events)

    def populate(self, events):
        for event in events:
            if (event.is_month_matching(self.month) and
                    event.is_group_matching(self.group)):
                self.add_event(event)

    def to_plain_list(self, interval):
        return [self.group, str(self.get_duration(interval))]


class MonthlyRaportHelper:

    def create_raports(self, events, month):
        to_return = []
        for group in config.group_dict:
            raport = MonthlyRaportForGroup(group, month, events)
            to_return.append(raport)
        return to_return

    def get_hours(self, month, raports):
        hours = 0.0
        for raport in self.get_raports(month, raports):
            hours = hours + raport.get_duration('hours')
        return hours

    def get_raports(self, month, raports):
        to_return = []
        for raport in raports:
            if raport.month == month:
                to_return.append(raport)
        return to_return
