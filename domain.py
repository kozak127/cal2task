import calendar
import icalendar
import math

import config


class Events:

    def __init__(self):
        self.list = []
        self.populate()

    def populate(self):
        calendar_file = open(config.cal_file, 'rb')
        parsed_calendar = icalendar.Calendar.from_ical(calendar_file.read())

        for component in parsed_calendar.walk('vevent'):
            dtstart = component['dtstart'].dt
            dtend = component['dtend'].dt
            raw_summary = component['SUMMARY'].split(config.cal_delimeter, 1)
            group = raw_summary[0].lower()
            if len(raw_summary) > 1:
                summary = raw_summary[1]
            else:
                summary = ""

            if (dtstart.year == config.year and dtstart.month == config.month):
                self.list.append(Event(group, summary, dtstart, dtend))

        calendar_file.close()

    def get_invalid_events(self):
        invalid_events_list = []

        for event in self.list:
            if (event.is_valid() is False):
                invalid_events_list.append(event)

        if len(invalid_events_list) == 0:
            return None
        else:
            return invalid_events_list


class DailySummaries:

    def __init__(self, events_list):
        self.list = []
        self.populate(events_list)

    def populate(self, events_list):
        days = xrange(1, calendar.monthrange(config.year, config.month)[1] + 1)
        for day in days:
            for group in config.group_dict:
                summary = DailyGroupSummary(group, day, events_list)
                self.list.append(summary)

    def get_hours_for_day(self, day):
        hours = 0
        for summary in self.list:
            if summary.day == day:
                hours = hours + summary.get_duration_in_hours()
        return hours

    def get_summaries_for_day(self, day):
        summaries = []
        for summary in self.list:
            if summary.day == day:
                summaries.append(summary)
        return summaries


class MonthlySummaries:

    def __init__(self, daily_summaries_list):
        self.list = []
        self.populate(daily_summaries_list)

    def populate(self, daily_summaries_list):
        for group in config.group_dict:
            summary = MonthlyGroupSummary(group, daily_summaries_list)
            self.list.append(summary)

    def get_hours(self):
        hours = 0
        for summary in self.list:
            hours = hours + summary.hours
        return hours


class Event:

    def __init__(self, group, summary, dtstart, dtend):
        self.group = group
        self.summary = summary
        self.dtstart = dtstart
        self.dtend = dtend

    def get_duration_in_minutes(self):
        duration = self.dtend - self.dtstart
        return (duration.seconds) // 60

    def is_valid(self):
        for group in config.group_dict:
            if (self.is_group_matching(group) is True):
                return True
        return False

    def is_group_matching(self, group):
        if (config.subgroups is False and self.group == group):
            return True
        if (config.subgroups is True and group.find(self.group) > -1):
            return True

        return False

    def to_plain_list(self):
        return [self.dtstart.strftime('%Y-%m-%d'), self.group, self.summary]


class DailyGroupSummary:

    def __init__(self, group, day, event_list):
        self.group = group
        self.day = day
        self.minutes = 0
        self.summary = ""
        self.populate(event_list)

    def populate(self, event_list):
        for event in event_list:
            if (event.dtstart.day == self.day and
                    event.is_group_matching(self.group)):
                self.add_event(event)
        self.remove_trailing_summary_delimeter()

    def add_event(self, event):
        self.minutes = self.minutes + event.get_duration_in_minutes()
        self.summary = self.summary + event.summary + config.summary_delimeter

    def get_duration_in_hours(self):
        return int(math.ceil(float(self.minutes) / 60))  # rounded up

    def remove_trailing_summary_delimeter(self):
        self.summary = self.summary[:-2]

    def to_plain_list(self):
        return [str(self.get_duration_in_hours()), self.summary]


class MonthlyGroupSummary:

    def __init__(self, group, daily_list):
        self.group = group
        self.hours = 0
        self.populate(daily_list)

    def populate(self, daily_list):
        for daily in daily_list:
            if daily.group == self.group:
                self.add_daily_summary(daily)

    def add_daily_summary(self, daily_summary):
        self.hours = self.hours + daily_summary.get_duration_in_hours()

    def to_plain_list(self):
        return [self.group, str(self.hours)]
