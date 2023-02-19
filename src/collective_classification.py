# IMPORTS
from constants import *
from assign_management_levels_enron import *
from main.network.social_network import create_network
from main.visualization.random_baseline_enron import *

from main.algorithms.collective_classification import *
import main.algorithms.NodeInfo
import main.algorithms.ModelInfo
from main.visualization.plot_collective_classification import PlotCollectiveClassification

import warnings
warnings.filterwarnings('ignore')


# To find the best utility score experiment was
# carried out for all calculated features, as well as the best Jaccard value and threshold were chosen from
# a range of different values
pcts = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1] # percentage of known nodes used for classifications
thresholds = [2, 3, 4, 5, 6, 7, 8, 9, 10] # different values of threshold used to prevent domination of majority classes
jaccard_mins = [0.7, 0.8, 0.9, 0.99] # minimum values for jaccard coefficient as one of the iteration end conditions
levels = [2,3] # company management levels
minority_labels = []

positions = pd.read_csv(ENRON_FILE_FLATTEN_HIERARCHY, sep=';')

# cast FLATTEN_POSITION keyword to POSITION keyword
positions = positions[[FLATTEN_POSITION]]
positions.columns = [POSITION]


# COLLECTIVE CLASSIFICATION
for month in [1]:
    features = pd.read_csv(ENRON_FILE_FEATURES.format(month), sep=';', index_col=ID)

    emails = pd.read_csv(ENRON_FILE_MINIMUM_ACTIVITY.format(month), sep=';')
    G = create_network(emails, weight=False)

    # label propagation needs network graph to be undirected
    G_undirected = G.to_undirected()

    for level in [3]:
        _features = assign_management_levels_enron(level, features, positions)
        for pct in [0.9]:
            for threshold in thresholds:
                for jaccard_min in jaccard_mins:
                    collective_classification(month, G_undirected, _features.copy(), pct, level, threshold,
                                              minority_labels, jaccard_min)

plot = PlotCollectiveClassification(levels[1], random_baseline_enron)
plot.plot()