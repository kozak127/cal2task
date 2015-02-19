import config
import event
import report
import misc
import output

# get file from url
if config.cal_download_file is True:
    misc.download_file(config.cal_url, config.cal_file)

# read data from file
reader = event.CalFileReader(config.cal_file, config.cal_delimeter)
events = reader.read_events(config.month, config.year)

# validate data
validator = event.EventValidator(config.group_dict)
invalid_events = validator.get_invalid_events(events)

# process data
daily_helper = report.DailyReportHelper()
weekly_helper = report.WeeklyReportHelper()
monthly_helper = report.MonthlyReportHelper()
daily_reports = daily_helper.create_reports(events, config.month, config.year)
weekly_reports = weekly_helper.create_reports(events, config.month, config.year)
monthly_reports = monthly_helper.create_reports(events, config.month)

# prepare output
out = None
if config.output == 'console':
    out = output.ConsoleOutput()
elif config.output == 'csv':
    out = output.CsvOutput()
elif config.output == 'xml':
    out = output.XmlOutput()

# print data to output
if invalid_events is not None:
    out.process_invalid_events(invalid_events)

out.process_daily_reports(daily_reports)
out.process_weekly_reports(weekly_reports)
out.process_monthly_reports(monthly_reports)
