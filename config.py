# if in group dict are combined groups, for example 'group1, group2', 'group3'
subgroups = True

# available values: console, csv, none
output = 'csv'

# default time to look in calendar file
month = 9
year = 2014

summary_delimeter = ', '  # used when combining more summaries into one

# CSV options
csv_delimeter = ';'  # only ONE char
csv_directory = '.'  # please use existing directory
csv_divide_weeks = True

# iCAL options
cal_delimeter = ' - '  # group<delimeter>task in calendar event
cal_download_file = True  # download new file
cal_file = 'basic.ics'  # filename with calendar
# url to download file
cal_url = "http address from google calendar"

group_dict = ['project_1', 'project_2_sub_1, project_2_sub_2', 'project_3_sub_1, project_3_sub_2']
