import calendar

import config
import misc


class ReportItem:

    def __init__(self, *args, **kwargs):
        self.set_summary(kwargs.get('summary', ''))
        self.set_time(kwargs.get('time', 0.0))

    def set_summary(self, summary):
        self.summary = summary

    def set_time(self, time):
        self.time = float(time)

    def is_summary_equal(self, report):
        return self.summary == report.summary

    def join(self, report):
        self.time+=report.time

    def __str__(self):
        if config.summary_with_time:
            return config.summary_time_delimeter.join([self.summary, str(round(self.time / 60.0, 2))])
        return self.summary


class Report:

    def __init__(self, group):
        self.minutes = 0.0
        self.summary = list()
        self.group = group

    def populate(self, events):
        raise NotImplementedError("populate")

    def to_plain_list(self, interval):
        return [str(self.get_duration(interval)), config.summary_delimeter.join([str(s) for s in self.summary])]

    def get_duration(self, interval):
        if interval == 'hours':
            return round(self.minutes / 60.0, 2)
        elif interval == 'minutes':
            return self.minutes
        else:
            return self.minutes

    def add_event(self, event):
        self.minutes = self.minutes + event.get_duration()
        new_report = ReportItem(summary=event.summary, time=event.get_duration())
        if (config.summary_join_similar):
            similar = [report for report in self.summary if report.is_summary_equal(new_report)]
            if (any(similar)):
                similar[0].join(new_report)
                return
        # if do not join similar or no similar was foud
        self.summary.append(new_report)


class DailyReportForGroup(Report):

    def __init__(self, group, day, events):
        Report.__init__(self, group)
        self.day = day
        self.populate(events)

    def populate(self, events):
        for event in events:
            if (event.is_day_matching(self.day) and
                    event.is_group_matching(self.group)):
                self.add_event(event)


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
        Report.__init__(self, group)
        self.week = week
        self.populate(events)

    def populate(self, events):
        for event in events:
            if (event.is_week_matching(self.week) and
                    event.is_group_matching(self.group)):
                self.add_event(event)


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
        Report.__init__(self, group)
        self.month = month
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
