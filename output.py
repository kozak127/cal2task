import calendar
import csv
import datetime
import os

import config


class GeneralOutput:

    def process_monthly_summaries(self, monthly_summaries):
        pass

    def process_daily_summaries(self, daily_summaries):
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

    def process_monthly_summaries(self, monthly_summaries):
        print "=== MONTHLY SUMMARIES ==="
        for summary in monthly_summaries.list:
            print summary.group + " - " + str(summary.hours)
            print "-----------------"

    def process_daily_summaries(self, daily_summaries):
        print "=== DAILY SUMMARIES ==="
        for summary in daily_summaries.list:
            if summary.minutes != 0:
                print str(summary.day) + " - " + summary.group
                print str(summary.get_duration_in_hours()) + " - " + \
                    summary.summary
                print "-----------------"

    def process_invalid_events(self, event_list):
        print "=== INVALID EVENTS:  ==="
        for event in event_list:
            print event.group + " - " + event.summary + \
                " - " + event.dtstart.strftime('%Y-%m-%d')
            print "-----------------"


class CsvOutput(GeneralOutput):

    def __init__(self):
        self.delimeter = config.csv_delimeter

    def process_monthly_summaries(self, monthly_summaries):
        csv_file_path = self.generateFilepath('monthly', '.csv')
        data = []
        heading = ['GROUP', 'HOURS']

        for summary in monthly_summaries.list:
            data.append(summary.to_plain_list())
        data.append(['TOTAL', str(monthly_summaries.get_hours())])

        self.csv_writer(heading, data, csv_file_path, self.delimeter)

    def process_daily_summaries(self, daily_summaries):
        csv_file_path = self.generateFilepath('daily', '.csv')
        data = []

        heading = ['TOTAL', '###', 'DAY', '###']
        for group in config.group_dict:
            heading.append('###')
            heading.append(group.upper())

        days = xrange(1, calendar.monthrange(config.year, config.month)[1] + 1)
        for day in days:
            data_row = []
            data_row.append(str(daily_summaries.get_hours_for_day(day)))
            data_row.append('   ')
            data_row.append(str(day))
            data_row.append('   ')

            for summary in daily_summaries.get_summaries_for_day(day):
                data_row = data_row + summary.to_plain_list()

            data.append(data_row)

            if config.csv_divide_weeks is True:
                date = datetime.date(config.year, config.month, day)
                if date.strftime("%A") == "Sunday":
                    data.append([''])

        self.csv_writer(heading, data, csv_file_path, self.delimeter)

    def process_invalid_events(self, event_list):
        csv_file_path = self.generateFilepath('invalid', '.csv')
        data = []
        heading = ['date', 'group', 'summary']

        for event in event_list:
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
