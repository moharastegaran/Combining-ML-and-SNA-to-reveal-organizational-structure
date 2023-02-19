# IMPORTS
import pandas as pd
from constants import *
from data_loader import *
from data_cleaner import *


# DATA CLEANING
employees = load_employees()
emails = load_emails()

employees, emails = delete_nan(employees, emails)

# Update emails with documented methods in data_cleaner.py
emails = remap_employee_ids(employees, emails)
emails = delete_messages_sent_to_yourself(emails)
emails = delete_messages_with_boundary_dates(emails)
emails = emails.drop_duplicates([SENDER, RECIPIENT, EVENT_DATE])

# MINIMUM EMPLOYEE ACTIVITY
# Add Year & Month columns for emails communications to filter emails based on minimum activity
emails[MONTH] = emails[EVENT_DATE].apply(lambda x: x.month)
emails[YEAR] = emails[EVENT_DATE].apply(lambda x: x.year)

# Filter emails based on minimum activity
for month in MONTHS:
    emails = remove_employees_below_minimum_activity(emails, month)
    emails.to_csv(ENRON_FILE_MINIMUM_ACTIVITY.format(month), sep=';', index=False)



# FLATTENING THE HIERARCHY
# Enron dataset consists of more than 3 level hierarchy
# Here we only examine three and two levels of employees hierarchy
# So we flatten it to three levels max
employees[FLATTEN_POSITION] = -1

first_management_level = ['CEO', 'President', 'Vice President']
second_management_level = ['Director', 'Managing Director', 'Manager']
standard_employee = ['Employee', 'In House Lawyer', 'Trader']

employees.loc[employees[POSITION].isin(first_management_level), FLATTEN_POSITION] = 1
employees.loc[employees[POSITION].isin(second_management_level), FLATTEN_POSITION] = 2
employees.loc[employees[POSITION].isin(standard_employee), FLATTEN_POSITION] = 3

employees.to_csv(ENRON_FILE_FLATTEN_HIERARCHY, sep=';', index=False)