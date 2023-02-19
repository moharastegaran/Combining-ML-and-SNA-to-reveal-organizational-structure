# IMPORTS
import pandas as pd

# from constants import *
from data_cleaner import *
from main.network.neighborhood_variability import *


import warnings
warnings.filterwarnings('ignore')

# CREATE FEATURES
for month in MONTHS:
    df = pd.read_csv(ENRON_FILE_MINIMUM_ACTIVITY.format(month), sep=';', parse_dates=[EVENT_DATE])

    work_at_weekend = calculate_work_at_weekend(df)

    network_measures = pd.read_csv(ENRON_FILE_NETWORK_MEASURES.format(month), sep=';')

    features = pd.merge(network_measures, work_at_weekend, left_on=ID, right_on=SENDER)

    print(len(features[ID]))
    nv_sender, nv_recipient, nv_sender_recipient = calculate_neighborhood_variability(df, features[ID])
    nv_sender = pd.DataFrame.from_dict(nv_sender, orient='index', columns=[NEIGHBORHOOD_VARIABILITY_SENDER])
    nv_sender.index.name = ID

    nv_recipient = pd.DataFrame.from_dict(nv_recipient, orient='index', columns=[NEIGHBORHOOD_VARIABILITY_RECIPIENT])
    nv_recipient.index.name = ID

    nv_sender_recipient = pd.DataFrame.from_dict(nv_sender_recipient, orient='index', columns=[NEIGHBORHOOD_VARIABILITY_ALL])
    nv_sender_recipient.index.name = ID

    features = pd.merge(features, nv_sender, on=ID)
    features = pd.merge(features, nv_recipient, on=ID)
    features = pd.merge(features, nv_sender_recipient, on=ID)

    features.to_csv(ENRON_FILE_FEATURES.format(month), sep=';', index=False)


