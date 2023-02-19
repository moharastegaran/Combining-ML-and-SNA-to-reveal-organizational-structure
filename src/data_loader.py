import pandas as pd
from constants import *
from main.root_dir import data_root


def load_employees():
    """
    The function to load list of employees into pandas DataFrame from enron dataset

    :rtype: pandas.DataFrame
    """
    employees = pd.read_csv(data_root()+r'\enron\raw\employees.txt', sep=';', header=None)
    employees.index.name = ID
    employees.columns = [EMAIL, NAME, POSITION, DETAILS]
    return employees

def load_emails():
    """
    The function to load list of emails exchanged between employees into pandas DataFrame
    from enron dataset

    :rtype: pandas.DataFrame
    """
    emails = pd.read_csv(data_root()+r'\enron\raw\emails.linesnum', sep=' ', header=None)
    emails.columns = [EVENT_DATE, SENDER, RECIPIENT]
    emails[EVENT_DATE] = pd.to_datetime(emails[EVENT_DATE], unit='s')
    return emails
