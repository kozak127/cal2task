# GENERAL options
output = 'csv'  # available values: console, csv, none
summary_delimeter = ', '  # used when combining more summaries into one
summary_with_time = True # include time in descriptions
summary_time_delimeter = ' - ' # used for combining time with descriptions
summary_join_similar = False # When on one day there are 2 tasks with the same summary they will apear as one. Time will be added up.
filename_pattern = "hours_%Y%M_%T"  # %Y - year, %M - month, %T - summary type (monthly, daily, invalid). Extension (csv, xls, etc) is added automatically
month = 12  # month to look in calendar file
year = 2014  # year to look in calendar file


# iCAL options
cal_delimeter = ' - '  # group<delimeter>task in calendar event
cal_download_file = True  # download new file
cal_file = 'basic.ics'  # filename with calendar
cal_url = "https://www.google.com/calendar/ical/_ SECURED :-) _/basic.ics"  # url to download file
group_dict = ['project1', 'project2_1', 'project2_2']
group_dict_remove_repeated_projects = True # when project exists twice on list will be counted twice. This flag prevent it.


# CSV options
csv_delimeter = ';'  # only ONE char
csv_directory = '.'  # please use existing directory
csv_divide_weeks = True
