import numpy as np
import pandas as pd
from sklearn.metrics import jaccard_score
from main.src.constants import *

def neighbors_per_month_sender(df, all_employees):
    """
    calculates sent neighborhood variability
    Return every neighbor of sender nodes ingraph per month

    :type df: already created dataFrame
    :type all_employees:
    """
    df_tmp = df.groupby([SENDER, df[EVENT_DATE].dt.year, df[EVENT_DATE].dt.month])[RECIPIENT].unique()
    df_tmp = pd.DataFrame(df_tmp)
    df_tmp.index.names = [ID, YEAR, MONTH]
    return fill_missing_neighbors(df_tmp, all_employees)


def neighbors_per_month_recipient(df, all_employees):
    """
    calculates received neighborhood variability
    Return every neighbor of recipient nodes ingraph per month

    :type df: already created dataFrame
    :type all_employees:
    :rtype:
    """
    df_tmp = df.groupby([RECIPIENT, df[EVENT_DATE].dt.year, df[EVENT_DATE].dt.month])[SENDER].unique()
    df_tmp = pd.DataFrame(df_tmp)
    df_tmp.index.names = [ID, YEAR, MONTH]
    return fill_missing_neighbors(df_tmp, all_employees)


def neighbors_per_month_sender_and_recipient(df_sender, df_recipient):
    """
    calculates sent & received (global) neighborhood variability
    Return every neighbor of nodes ingraph per month

    :type df: already created dataFrame
    :type all_employees:
    :rtype:
    """
    df_sender_recipient = pd.merge(df_sender, df_recipient, how='outer', on=[ID, YEAR, MONTH]).sort_index()
    df_sender_recipient = df_sender_recipient.apply(merge_contacted_ids, axis=1)
    df_sender_recipient = pd.DataFrame(df_sender_recipient)
    df_sender_recipient.index.names = [ID, YEAR, MONTH]
    return df_sender_recipient


def merge_contacted_ids(row):
    if row[0] is np.NaN:
        return row[1]
    if row[1] is np.NaN:
        return row[0]
    sent = np.array(row[0])
    received = np.array(row[1])
    return sent | received


def fill_missing_neighbors(df, all_employees):
    df.iloc[:, 0] = df.apply(lambda row: all_employees.isin(row[0]).tolist(), axis=1)
    return df


def calculate_neighborhood_variability(df, all_employees):
    """
    Calculate jaccard coefficient for every neighborhood variability
    :rtype: three dataFrames consists of different forms of neighborhood variability
    """
    df_sender = neighbors_per_month_sender(df, all_employees)
    df_recipient = neighbors_per_month_recipient(df, all_employees)
    df_sender_recipient = neighbors_per_month_sender_and_recipient(df_sender, df_recipient)

    neighborhood_variability_sender = calculate_jaccard(df_sender)
    neighborhood_variability_recipient = calculate_jaccard(df_recipient)
    neighborhood_variability_sender_recipient = calculate_jaccard(df_sender_recipient)

    return neighborhood_variability_sender, neighborhood_variability_recipient, neighborhood_variability_sender_recipient

def calculate_jaccard(df):
    employee_ids = df.index.get_level_values(0).unique()

    neighborhood_variability = dict()

    for id in employee_ids:
        row = df.loc[(id, slice(None), slice(None))]
        neighborhood_variability[id] = jaccard(row, id)

    return neighborhood_variability


def jaccard(rows, employee_id):

    if len(rows) < 2:
        return 0

    jaccard = []
    years = rows.index.get_level_values(1).unique()

    for year in range(len(years)):
        months = rows.loc[(employee_id, years[year], slice(None))].index.get_level_values(0).unique()

        for month_nr in range(len(months)):
            if (month_nr == len(months) - 1) & (year == len(years) - 1):
                break

            if month_nr == len(months) - 1:
                current_set = rows.loc[(employee_id, years[year], months[month_nr])].tolist()[0]
                months = rows.loc[(employee_id, years[year + 1], slice(None))].index.get_level_values(0).unique()
                next_set = rows.loc[(employee_id, years[year + 1], months[0])].tolist()[0]
            else:
                current_set = rows.loc[(employee_id, years[year], months[month_nr])].tolist()[0]
                next_set = rows.loc[(employee_id, years[year], months[month_nr + 1])].tolist()[0]

            jaccard.append(jaccard_score(current_set, next_set))

    return np.median(jaccard)


