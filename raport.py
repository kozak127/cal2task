import calendar
import math

import config


class Raport:

    def __init__(self, group):
        self.minutes = 0.0
        self.summary = ""
        self.group = group

    def populate(self, events):
        pass

    def add_event(self, event):
        pass

    def to_plain_list(self, interval):
        pass

    def get_duration(self, interval):
        if interval == 'hours':
            return round(self.minutes / 60, 2)
        elif interval == 'minutes':
            return self.minutes
        else:
            return self.minutes

    def remove_trailing_summary_delimeter(self):
        self.summary = self.summary[:-2]


class DailyRaportForGroup(Raport):

    def __init__(self, group, day, events):
        self.group = group
        self.day = day
        self.minutes = 0.0
        self.summary = ""
        self.populate(events)

    def populate(self, events):
        for event in events:
            if (event.dtstart.day == self.day and
                    event.is_group_matching(self.group)):
                self.add_event(event)
        self.remove_trailing_summary_delimeter()

    def add_event(self, event):
        self.minutes = self.minutes + event.get_duration()
        self.summary = self.summary + event.summary + config.summary_delimeter

    def to_plain_list(self, interval):
        return [self.group, str(self.get_duration(interval)), self.summary]


class DailyRaportHelper:

    def create_raports(self, events, month, year):
        to_return = []
        days = xrange(1, calendar.monthrange(year, month)[1] + 1)
        for day in days:
            for group in config.group_dict:
                raport = DailyRaportForGroup(group, day, events)
                to_return.append(raport)
        return to_return

    def get_total_hours(self, day, raports):
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


class MonthlyRaportForGroup(Raport):

    def __init__(self, group, month, events):
        self.group = group
        self.minutes = 0.0
        self.month = month
        self.summary = ""
        self.populate(events)

    def populate(self, events):
        for event in events:
            if (event.dtstart.month == self.month and
                    event.is_group_matching(self.group)):
                self.add_event(event)

    def add_event(self, event):
        self.minutes = self.minutes + event.get_duration()
        self.summary = self.summary + event.summary + config.summary_delimeter

    def to_plain_list(self, interval):
        return [self.group, str(self.get_duration(interval))]


class MonthlyRaportHelper:

    def create_raports(self, events, month):
        to_return = []
        for group in config.group_dict:
            raport = MonthlyRaportForGroup(group, month, events)
            to_return.append(raport)
        return to_return

    def get_total_hours(self, month, raports):
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
