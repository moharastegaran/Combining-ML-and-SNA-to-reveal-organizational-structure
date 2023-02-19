import datetime
import pandas as pd
from constants import *


def delete_nan(employees, emails):
    """
    Delete rows from dataFrames with missing values
    Filter only emails with valid sender and receiver

    :type employees: pandas.DataFrame
    :type emails: pandas.DataFrame
    :rtype: object , copy of filtered dataFrames
    """
    employees = employees.dropna(axis=0, subset=[POSITION])
    employee_ids = employees.index
    emails = emails[emails[SENDER].isin(employee_ids) & emails[RECIPIENT].isin(employee_ids)]
    return employees.copy(), emails.copy()


def group_duplicates_email_addresses(employees):
    """
    Emails which share the same tuple of (NAME,POSITION,DETAILS)
    are grouped together to avoid duplication of emails to affect the classification task results

    :type employees: pandas.DataFrame
    :rtype: pandas.DataFrame
    """
    employees = employees.reset_index()
    return employees.groupby([NAME, POSITION, DETAILS])[ID].apply(list)


def remap_employee_ids(employees, emails):
    """
    Replace list of emails with mapping list of grouped emails
    to obtain more control over data

    :type employees: pandas.DataFrame
    :type emails: pandas.DataFrame
    :rtype: pandas.DataFrame
    """
    grouped_employees = group_duplicates_email_addresses(employees)

    id_map = {}

    def create_map_with_new_ids(row):
        more_than_one_id = len(row) > 1

        if more_than_one_id:
            first_id = row[0]
            other_ids = row[1:]

            id_map[first_id] = other_ids

    grouped_employees.apply(create_map_with_new_ids)

    # remap other ids to the first id
    new_ids = {k: oldk for oldk, oldv in id_map.items() for k in oldv}

    return emails.replace(new_ids)


def delete_messages_sent_to_yourself(emails):
    """
    Filter emails with the same recipient and sender

    :type emails: pandas.DataFrame
    :rtype: pandas.DataFrame , filtered emails
    """
    return emails[emails[SENDER] != emails[RECIPIENT]].copy()


def delete_messages_with_boundary_dates(emails):
    """
    Wrap emails with boundary date
    Select only emails which do not exceed the minimum and maximum date used for evaluation

    :type emails: pandas.DataFrame
    :rtype: pandas.DataFrame , filtered emails
    """
    after_enron_creation = emails[EVENT_DATE] >= pd.Timestamp(datetime.date(1985, 8, 1))
    before_enron_liquidation = emails[EVENT_DATE] < pd.Timestamp(datetime.date(2001, 12, 1))
    return emails[after_enron_creation & before_enron_liquidation].copy()


# weekend days
SATURDAY = 5
SUNDAY = 6



def remove_employees_below_minimum_activity(communication, months):
    """
    Filter communication of employees which period is below threshold months number
    To evaluate classification results based on minimum months of employees activity

    :type communication: pandas.DataFrame
    :type months: int
    :rtype: pandas.DataFrame
    """
    while True:
        communication_frequency = communication.drop_duplicates([SENDER, YEAR, MONTH]).groupby(SENDER).count()

        employees_under_threshold = communication_frequency[communication_frequency[MONTH] < months].index

        # drop employees who never sent or received an email
        at_least_one_message_sent = communication[RECIPIENT].isin(communication[SENDER])
        at_least_one_message_received = communication[SENDER].isin(communication[RECIPIENT])
        at_least_one_message_sent_and_received = at_least_one_message_sent & at_least_one_message_received

        if (len(communication[~at_least_one_message_sent_and_received]) > 0) | (len(employees_under_threshold) != 0):
            sender_above_threshold = ~communication[SENDER].isin(employees_under_threshold)
            recipient_above_threshold = ~communication[RECIPIENT].isin(employees_under_threshold)
            criteria = at_least_one_message_sent_and_received & sender_above_threshold & recipient_above_threshold
            communication = communication[criteria]
        else:
            break

    return communication


def calculate_work_at_weekend(df):
    """
    Calculate overwork at weekends, Saturday &  Sunday
    Group communicated emails on sender and sum up with previously created list of emails,(df)

    :type df: pandas.DataFrame
    :type months: int
    :rtype: pandas.DataFrame
    """
    df[WORK_AT_WEEKEND] = 0
    weekend_selector = (df[EVENT_DATE].dt.weekday == 5) | (df[EVENT_DATE].dt.weekday == 6) # SATURDAY=5, SUNDAY=6
    df.loc[weekend_selector, WORK_AT_WEEKEND] = 1
    df_weekend = df[[SENDER, WORK_AT_WEEKEND]].groupby(SENDER).sum()
    return pd.DataFrame(df_weekend, columns=[WORK_AT_WEEKEND])
