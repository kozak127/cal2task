import config
import domain
import misc
import output

# get file from url
if config.cal_download_file is True:
    misc.download_file(config.cal_url, config.cal_file)

# process data
events = domain.Events()
daily_summaries = domain.DailySummaries(events.list)
monthly_summaries = domain.MonthlySummaries(daily_summaries.list)
invalid_events = events.get_invalid_events()

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

out.process_daily_summaries(daily_summaries)
out.process_monthly_summaries(monthly_summaries)
