import calendar

import config
import misc


class Report:

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

    def remove_trailing_summary_delimiter(self):
        self.summary = self.summary[:-2]

    def add_event(self, event):
        self.minutes = self.minutes + event.get_duration()
        self.summary = self.summary + event.summary + config.summary_delimeter


class DailyReportForGroup(Report):

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
        self.remove_trailing_summary_delimiter()


class DailyReportHelper:

    def create_reports(self, events, month, year):
        to_return = []
        days = xrange(1, calendar.monthrange(year, month)[1] + 1)
        for day in days:
            for group in config.group_dict:
                report = DailyReportForGroup(group, day, events)
                to_return.append(report)
        return to_return

    def get_hours(self, day, reports):
        hours = 0.0
        for report in self.get_reports(day, reports):
            hours = hours + report.get_duration('hours')
        return hours

    def get_reports(self, day, reports):
        to_return = []
        for report in reports:
            if report.day == day:
                to_return.append(report)
        return to_return


class WeeklyReportForGroup(Report):

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
        self.remove_trailing_summary_delimiter()


class WeeklyReportHelper:

    def create_reports(self, events, month, year):
        to_return = []

        weeks = misc.get_week_numbers_in_month(month, year)
        for week in weeks:
            for group in config.group_dict:
                report = WeeklyReportForGroup(group, week, events)
                to_return.append(report)
        return to_return

    def get_hours(self, week, reports):
        hours = 0.0
        for report in self.get_reports(week, reports):
            hours = hours + report.get_duration('hours')
        return hours

    def get_reports(self, week, reports):
        to_return = []
        for report in reports:
            if report.week == week:
                to_return.append(report)
        return to_return


class MonthlyReportForGroup(Report):

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


class MonthlyReportHelper:

    def create_reports(self, events, month):
        to_return = []
        for group in config.group_dict:
            report = MonthlyReportForGroup(group, month, events)
            to_return.append(report)
        return to_return

    def get_hours(self, month, reports):
        hours = 0.0
        for report in self.get_reports(month, reports):
            hours = hours + report.get_duration('hours')
        return hours

    def get_reports(self, month, reports):
        to_return = []
        for report in reports:
            if report.month == month:
                to_return.append(report)
        return to_return
