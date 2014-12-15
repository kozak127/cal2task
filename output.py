import calendar
import csv
import datetime
import os

import config
import raport


class GeneralOutput:

    def process_monthly_raports(self, monthly_raports):
        pass

    def process_daily_raports(self, daily_raports):
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
        self.daily_raport_helper = raport.DailyRaportHelper()
        self.monthly_raport_helper = raport.MonthlyRaportHelper()

    def process_monthly_raports(self, raports):
        
        print "=== MONTHLY raports ==="
        for raport in raports:
            print raport.to_plain_list('hours')
            print "-----------------"
        print "~~~ MONTHLY TOTAL ~~~"
        print self.monthly_raport_helper.get_total_hours(config.month, raports)

    def process_daily_raports(self, raports):
        print "=== DAILY raports ==="
        for raport in raports:
            if raport.minutes != 0:
                print raport.to_plain_list('hours')
                print "-----------------"
        print "~~~ DAILY TOTAL ~~~"
        days = xrange(1, calendar.monthrange(config.year, config.month)[1] + 1)
        for day in days:
            print self.daily_raport_helper.get_total_hours(day, raports)

    def process_invalid_events(self, invalid_events):
        print "=== INVALID EVENTS:  ==="
        for event in invalid_events:
            print event.to_plain_list()
            print "-----------------"


class CsvOutput(GeneralOutput):

    def __init__(self):
        self.delimeter = config.csv_delimeter

    def process_monthly_raports(self, monthly_raports):
        csv_file_path = self.generateFilepath('monthly', '.csv')
        data = []
        heading = ['GROUP', 'HOURS']

        for summary in monthly_raports.list:
            data.append(summary.to_plain_list())
        data.append(['TOTAL', str(monthly_raports.get_hours())])

        self.csv_writer(heading, data, csv_file_path, self.delimeter)

    def process_daily_raports(self, daily_raports):
        csv_file_path = self.generateFilepath('daily', '.csv')
        data = []

        heading = ['TOTAL', '###', 'DAY', '###']
        for group in config.group_dict:
            heading.append('###')
            heading.append(group.upper())

        days = xrange(1, calendar.monthrange(config.year, config.month)[1] + 1)
        for day in days:
            data_row = []
            data_row.append(str(daily_raports.get_hours_for_day(day)))
            data_row.append('   ')
            data_row.append(str(day))
            data_row.append('   ')

            for summary in daily_raports.get_raports_for_day(day):
                data_row = data_row + summary.to_plain_list()

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
