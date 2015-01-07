import icalendar


class Event:

    def __init__(self, group, summary, dtstart, dtend):
        self.group = group
        self.summary = summary
        self.dtstart = dtstart
        self.dtend = dtend

    def get_duration(self):
        duration = self.dtend - self.dtstart
        return (duration.seconds) // 60

    def is_group_matching(self, group):
        if (group.find(self.group) > -1):
            return True

        return False

    def is_day_matching(self, day):
        if (self.dtstart.day == day):
            return True

        return False

    def is_week_matching(self, week):
        if (self.dtstart.isocalendar()[1] == week):
            return True

        return False

    def is_month_matching(self, month):
        if (self.dtstart.month == month):
            return True

        return False

    def to_plain_list(self):
        return [self.dtstart.strftime('%Y-%m-%d'), self.group, self.summary]


class CalFileReader:

    def __init__(self, file_patch, cal_delimeter):
        self.file_patch = file_patch
        self.cal_delimeter = cal_delimeter

    def read_events(self, month, year):
        events = []
        calendar_file = open(self.file_patch, 'rb')
        parsed_calendar = icalendar.Calendar.from_ical(calendar_file.read())

        for component in parsed_calendar.walk('vevent'):
            dtstart = component['dtstart'].dt
            dtend = component['dtend'].dt
            raw_summary = component['SUMMARY'].split(self.cal_delimeter, 1)
            group = raw_summary[0].lower()
            if len(raw_summary) > 1:
                summary = raw_summary[1]
            else:
                summary = ""

            if (dtstart.year == year and dtstart.month == month):
                events.append(Event(group, summary, dtstart, dtend))

        calendar_file.close()
        return events


class EventValidator:

    def __init__(self, groups):
        self.groups = groups

    def get_invalid_events(self, events):
        invalid_events_list = []

        for event in events:
            if (self.validate_event(event) is False):
                invalid_events_list.append(event)

        if len(invalid_events_list) == 0:
            return None
        else:
            return invalid_events_list

    def validate_event(self, event):
        for group in self.groups:
            if (event.is_group_matching(group) is True):
                return True
        return False

