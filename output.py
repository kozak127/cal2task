import calendar
import csv
import datetime
import os

import config
import report
import misc


class GeneralOutput:

    def process_monthly_reports(self, reports):
        pass

    def process_weekly_reports(self, reports):
        pass

    def process_daily_reports(self, reports):
        pass

    def process_invalid_events(self, event_list):
        pass

    @staticmethod
    def generate_filepath(case, filetype):
        directory = config.csv_directory
        filename = config.filename_pattern
        filename = filename.replace('%M', str(config.month))
        filename = filename.replace('%Y', str(config.year))
        filename = filename.replace('%T', case)
        filepath = directory + os.sep + filename + filetype
        return filepath


class ConsoleOutput(GeneralOutput):

    def __init__(self):
        self.daily_helper = report.DailyReportHelper()
        self.weekly_helper = report.WeeklyReportHelper()
        self.monthly_helper = report.MonthlyReportHelper()

    def process_monthly_reports(self, reports):
        print "=== MONTHLY reports ==="
        for report_instance in reports:
            print report_instance.to_plain_list('hours')
            print "-----------------"
        print "~~~ MONTHLY TOTAL ~~~"
        print self.monthly_helper.get_hours(config.month, reports)

    def process_weekly_reports(self, reports):
        print "=== WEEKLY reports ==="
        for report_instance in reports:
            if report_instance.minutes != 0:
                print report_instance.to_plain_list('hours')
                print "-----------------"
        print "~~~ WEEKLY TOTAL ~~~"

        weeks = misc.get_week_numbers_in_month(config.month, config.year)
        for week in weeks:
            print self.weekly_helper.get_hours(week, reports)

    def process_daily_reports(self, reports):
        print "=== DAILY reports ==="
        for report_instance in reports:
            if report_instance.minutes != 0:
                print report_instance.to_plain_list('hours')
                print "-----------------"
        print "~~~ DAILY TOTAL ~~~"
        days = xrange(1, calendar.monthrange(config.year, config.month)[1] + 1)
        for day in days:
            print self.daily_helper.get_hours(day, reports)

    def process_invalid_events(self, invalid_events):
        print "=== INVALID EVENTS:  ==="
        for event in invalid_events:
            print event.to_plain_list()
            print "-----------------"


class CsvOutput(GeneralOutput):

    def __init__(self):
        self.delimeter = config.csv_delimeter
        self.daily_helper = report.DailyReportHelper()
        self.weekly_helper = report.WeeklyReportHelper()
        self.monthly_helper = report.MonthlyReportHelper()

    def process_monthly_reports(self, reports):
        csv_file_path = self.generate_filepath('monthly', '.csv')
        data = []
        heading = ['GROUP', 'HOURS']

        for report_instance in reports:
            data.append(report_instance.to_plain_list('hours'))

        total_hours = str(self.monthly_helper.get_hours(config.month, reports))
        data.append(['TOTAL', total_hours])

        self.csv_writer(heading, data, csv_file_path, self.delimeter)

    def process_weekly_reports(self, reports):
        csv_file_path = self.generate_filepath('weekly', '.csv')
        data = []

        heading = ['TOTAL', '###', 'WEEK', '###']
        for group in config.group_dict:
            heading.append('###')
            heading.append(group.upper())

        weeks = misc.get_week_numbers_in_month(config.month, config.year)
        for week in weeks:
            data_row = []
            data_row.append(str(self.weekly_helper.get_hours(week, reports)))
            data_row.append('   ')
            data_row.append(str(week))
            data_row.append('   ')

            for report_instance in self.weekly_helper.get_reports(week, reports):
                data_row = data_row + report_instance.to_plain_list("hours")
            data.append(data_row)

        self.csv_writer(heading, data, csv_file_path, self.delimeter)

    def process_daily_reports(self, reports):
        csv_file_path = self.generate_filepath('daily', '.csv')
        data = []

        heading = ['TOTAL', '###', 'DAY', '###']
        for group in config.group_dict:
            heading.append('###')
            heading.append(group.upper())

        days = xrange(1, calendar.monthrange(config.year, config.month)[1] + 1)
        for day in days:
            data_row = []
            data_row.append(str(self.daily_helper.get_hours(day, reports)))
            data_row.append('   ')
            data_row.append(str(day))
            data_row.append('   ')

            for report_instance in self.daily_helper.get_reports(day, reports):
                data_row = data_row + report_instance.to_plain_list("hours")
            data.append(data_row)

            if config.csv_divide_weeks is True:
                date = datetime.date(config.year, config.month, day)
                if date.strftime("%A") == "Sunday":
                    data.append([''])

        self.csv_writer(heading, data, csv_file_path, self.delimeter)

    def process_invalid_events(self, invalid_events):
        csv_file_path = self.generate_filepath('invalid', '.csv')
        data = []
        heading = ['date', 'group', 'summary']

        for event in invalid_events:
            data.append(event.to_plain_list())

        self.csv_writer(heading, data, csv_file_path, self.delimeter)

    @staticmethod
    def csv_writer(heading, data, path, delimiter):
        with open(path, "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter)
            heading = [s.encode('utf-8') for s in heading]
            writer.writerow(heading)
            for line in data:
                line = [s.encode('utf-8') for s in line]
                writer.writerow(line)
