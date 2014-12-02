# GENERAL options
subgroups = True # if in group dict are combined groups, for example 'group1, group2', 'group3'
output = 'csv' # available values: console, csv, none
summary_delimeter = ', '  # used when combining more summaries into one
filename_pattern = "worked_hours_%Y%M_%T" # %Y - year, %M - month, %T - summary type (monthly, daily, invalid). Extension (csv, xls, etc) is added automatically
month = 11 # month to look in calendar file
year = 2014 # year to look in calendar file


# iCAL options
cal_delimeter = ' - '  # group<delimeter>task in calendar event
cal_download_file = True  # download new file
cal_file = 'basic.ics'  # file with calendar
cal_url = "http address from google calendar" # url to download file
group_dict = ['project_1', 'project_2_sub_1, project_2_sub_2', 'project_3_sub_1, project_3_sub_2']


# CSV options
csv_delimeter = ';'  # only ONE char
csv_directory = '.'  # please use existing directory
csv_divide_weeks = True