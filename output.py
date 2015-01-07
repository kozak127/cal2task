import calendar
import csv
import datetime
import os

import config
import raport
import misc


class GeneralOutput:

    def process_monthly_raports(self, raports):
        pass

    def process_weekly_raports(self, raports):
        pass

    def process_daily_raports(self, raports):
        pass

    def process_invalid_events(self, event_list):
        pass

    def generateFilepath(self, case, filetype):
        directory = config.csv_directory
        filename = config.filename_pattern
        filename = filename.replace('%M', str(config.month))
        filename = filename.replace('%Y', str(config.year))
        filename = filename.replace('%T', case)
        filepath = directory + os.sep + filename + filetype
        return filepath


class ConsoleOutput(GeneralOutput):

    def __init__(self):
        self.daily_helper = raport.DailyRaportHelper()
        self.weekly_helper = raport.WeeklyRaportHelper()
        self.monthly_helper = raport.MonthlyRaportHelper()

    def process_monthly_raports(self, raports):
        print "=== MONTHLY raports ==="
        for raport_instance in raports:
            print raport_instance.to_plain_list('hours')
            print "-----------------"
        print "~~~ MONTHLY TOTAL ~~~"
        print self.monthly_helper.get_hours(config.month, raports)

    def process_weekly_raports(self, raports):
        print "=== WEEKLY raports ==="
        for raport_instance in raports:
            if raport_instance.minutes != 0:
                print raport_instance.to_plain_list('hours')
                print "-----------------"
        print "~~~ WEEKLY TOTAL ~~~"

        weeks = misc.getWeekNumbersInMonth(config.month, config.year)
        for week in weeks:
            print self.weekly_helper.get_hours(week, raports)

    def process_daily_raports(self, raports):
        print "=== DAILY raports ==="
        for raport_instance in raports:
            if raport_instance.minutes != 0:
                print raport_instance.to_plain_list('hours')
                print "-----------------"
        print "~~~ DAILY TOTAL ~~~"
        days = xrange(1, calendar.monthrange(config.year, config.month)[1] + 1)
        for day in days:
            print self.daily_helper.get_hours(day, raports)

    def process_invalid_events(self, invalid_events):
        print "=== INVALID EVENTS:  ==="
        for event in invalid_events:
            print event.to_plain_list()
            print "-----------------"


class CsvOutput(GeneralOutput):

    def __init__(self):
        self.delimeter = config.csv_delimeter
        self.daily_helper = raport.DailyRaportHelper()
        self.weekly_helper = raport.WeeklyRaportHelper()
        self.monthly_helper = raport.MonthlyRaportHelper()

    def process_monthly_raports(self, raports):
        csv_file_path = self.generateFilepath('monthly', '.csv')
        data = []
        heading = ['GROUP', 'HOURS']

        for raport_instance in raports:
            data.append(raport_instance.to_plain_list('hours'))

        total_hours = str(self.monthly_helper.get_hours(config.month, raports))
        data.append(['TOTAL', total_hours])

        self.csv_writer(heading, data, csv_file_path, self.delimeter)

    def process_weekly_raports(self, raports):
        csv_file_path = self.generateFilepath('weekly', '.csv')
        data = []

        heading = ['TOTAL', '###', 'WEEK', '###']
        for group in config.group_dict:
            heading.append('###')
            heading.append(group.upper())

        weeks = misc.getWeekNumbersInMonth(config.month, config.year)
        for week in weeks:
            data_row = []
            data_row.append(str(self.weekly_helper.get_hours(week, raports)))
            data_row.append('   ')
            data_row.append(str(week))
            data_row.append('   ')

            for raport_instance in self.weekly_helper.get_raports(week, raports):
                data_row = data_row + raport_instance.to_plain_list("hours")
            data.append(data_row)

        self.csv_writer(heading, data, csv_file_path, self.delimeter)

    def process_daily_raports(self, raports):
        csv_file_path = self.generateFilepath('daily', '.csv')
        data = []

        heading = ['TOTAL', '###', 'DAY', '###']
        for group in config.group_dict:
            heading.append('###')
            heading.append(group.upper())

        days = xrange(1, calendar.monthrange(config.year, config.month)[1] + 1)
        for day in days:
            data_row = []
            data_row.append(str(self.daily_helper.get_hours(day, raports)))
            data_row.append('   ')
            data_row.append(str(day))
            data_row.append('   ')

            for raport_instance in self.daily_helper.get_raports(day, raports):
                data_row = data_row + raport_instance.to_plain_list("hours")
            data.append(data_row)

            if config.csv_divide_weeks is True:
                date = datetime.date(config.year, config.month, day)
                if date.strftime("%A") == "Sunday":
                    data.append([''])

        self.csv_writer(heading, data, csv_file_path, self.delimeter)

    def process_invalid_events(self, invalid_events):
        csv_file_path = self.generateFilepath('invalid', '.csv')
        data = []
        heading = ['date', 'group', 'summary']

        for event in invalid_events:
            data.append(event.to_plain_list())

        self.csv_writer(heading, data, csv_file_path, self.delimeter)

    def csv_writer(self, heading, data, path, delimeter):
        with open(path, "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=delimeter)
            heading = [s.encode('utf-8') for s in heading]
            writer.writerow(heading)
            for line in data:
                line = [s.encode('utf-8') for s in line]
                writer.writerow(line)
