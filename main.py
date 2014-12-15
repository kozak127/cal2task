import config
import event
import raport
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
daily_helper = raport.DailyRaportHelper()
monthly_helper = raport.MonthlyRaportHelper()
daily_raports = daily_helper.create_raports(events, config.month, config.year)
monthly_raports = monthly_helper.create_raports(events, config.month)

# prepare output
out = None
if (config.output == 'console'):
    out = output.ConsoleOutput()
elif (config.output == 'csv'):
    out = output.CsvOutput()
elif (config.output == 'xml'):
    out = output.XmlOutput()

# print data to output
if invalid_events is not None:
    out.process_invalid_events(invalid_events)

out.process_daily_raports(daily_raports)
out.process_monthly_raports(monthly_raports)
