from main.root_dir import data_root
ROOT_DIR = data_root()


# NUMBER OF MONTHS
MONTHS = [1,2,3,4,5]

# LABELS
SENDER = 'Sender'
RECIPIENT = 'Recipient'
EVENT_DATE = 'EventDate'
ID = 'ID'
REPORTS_TO_ID = 'ReportsToID'
POSITION = 'ManagementLevel'
YEAR = 'year'
MONTH = 'month'

WEIGHT = 'weight'

# NETWORK MEASURES
IN_DEGREE = 'in_degree'
OUT_DEGREE = 'out_degree'
BETWEENNESS = 'betweenness'
CLOSENESS = 'closeness'
EIGENVECTOR = 'eigenvector'
CLUSTERING = 'clustering_coeff'
PAGERANK = 'pagerank'
HUBS = 'hubs'
AUTHORITIES = 'authorities'
CLIQUES_COUNT = 'cliques_count'
MAX_CLIQUE = 'max_clique'

# OTHER FEATURES
OVERTIME = 'overtime'
WORK_AT_WEEKEND = 'work_at_weekend'
NEIGHBORHOOD_VARIABILITY_SENDER = 'neighborhood_variability_sender'
NEIGHBORHOOD_VARIABILITY_RECIPIENT = 'neighborhood_variability_recipient'
NEIGHBORHOOD_VARIABILITY_ALL = 'neighborhood_variability_all'

#ENRON DATASET CONSTS
ENRON_FILE_MINIMUM_ACTIVITY = ROOT_DIR +'\enron\processed\minimum_activity\months_{0}.csv'
ENRON_FILE_FLATTEN_HIERARCHY = ROOT_DIR+'\enron\processed\hierarchy_flatten.csv'
ENRON_FILE_NETWORK_MEASURES = ROOT_DIR+r'\enron\processed\network_measures\months_{0}.csv'
ENRON_FILE_FEATURES = ROOT_DIR+r'\enron\processed\features\months_{0}.csv'


EMAIL = 'email'
NAME = 'name'
DETAILS = 'details'
FLATTEN_POSITION = 'flattenManagementLevels'