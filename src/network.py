# IMPORTS
from constants import *
from main.network.social_network import *


# CALCULATE NETWORK MEASURES
for month in MONTHS:
    df = pd.read_csv(ENRON_FILE_MINIMUM_ACTIVITY.format(month), sep=';')
    df = calculate_weights(df)
    G = create_network(df, weight=True)
    df = calculate_network_measures(G)
    df.to_csv(ENRON_FILE_NETWORK_MEASURES.format(month), sep=';', index=False)
