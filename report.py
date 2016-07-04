import calendar

import config
import misc


class Report:

    def __init__(self, group):
        self.minutes = 0.0
        self.summary = ""
        self.group = group

    def populate(self, events):
        raise NotImplementedError("populate")

    def to_plain_list(self, interval):
        return [str(self.get_duration(interval)), self.summary]

    def get_duration(self, interval):
        if interval == 'hours':
            return round(self.minutes / 60.0, 2)
        elif interval == 'minutes':
            return self.minutes
        else:
            return self.minutes

    def remove_trailing_summary_delimiter(self):
        remove_last = len(config.summary_delimeter)
        self.summary = self.summary[:-remove_last]

    def add_event(self, event):
        summary = [
            self.summary,
            event.summary
        ]
        if config.summary_with_time:
            summary.extend([
                config.summary_time_delimeter,
                str(round(event.get_duration() / 60.0, 2))
            ])
        summary.append(config.summary_delimeter)

        self.minutes = self.minutes + event.get_duration()
        self.summary = "".join(summary)


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
        Report.__init__(self, group)
        self.week = week
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
