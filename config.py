# GENERAL options
output = 'csv'  # available values: console, csv, none
summary_delimeter = ', '  # used when combining more summaries into one
filename_pattern = "hours_%Y%M_%T"  # %Y - year, %M - month, %T - summary type (monthly, daily, invalid). Extension (csv, xls, etc) is added automatically
month = 12  # month to look in calendar file
year = 2014  # year to look in calendar file


# iCAL options
cal_delimeter = ' - '  # group<delimeter>task in calendar event
cal_download_file = True  # download new file
cal_file = 'basic.ics'  # filename with calendar
cal_url = "https://www.google.com/calendar/ical/_ SECURED :-) _/basic.ics"  # url to download file
group_dict = ['project1', 'project2_1, project2_2']


# CSV options
csv_delimeter = ';'  # only ONE char
csv_directory = '.'  # please use existing directory
csv_divide_weeks = True
