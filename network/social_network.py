import pandas as pd
import networkx as nx
from networkx.algorithms.clique import cliques_containing_node, node_clique_number

from main.src.constants import *


def calculate_weights(df):
    """
    Weigh each & every communicated email to get it ready for network creation

    """
    messages_send_to_specific_employee = df.groupby([SENDER, RECIPIENT]).size().reset_index()
    all_sent_messages = df.groupby(SENDER).size().reset_index()

    weights_df = messages_send_to_specific_employee.merge(all_sent_messages, on=SENDER)
    weights_df[WEIGHT] = weights_df['0_x'] / weights_df['0_y']

    df = df.merge(weights_df, on=[SENDER, RECIPIENT])

    # drop duplicates in data frame with emails to get the edges of the graph with calculated weights
    df = df.drop_duplicates([SENDER, RECIPIENT])

    return df[[SENDER, RECIPIENT, WEIGHT]]


def create_network(df, weight):
    """
    Return a graph from pandas dataFrame based on weights of edges
    Here, Edges are every communicated email

    :type df: pandas.dataFrame
    :type weight: boolean to declare weight state
    :rtype: networkx.dataFrame
    """
    if weight :
        return nx.from_pandas_edgelist(df, source=SENDER, target=RECIPIENT, edge_attr=WEIGHT, create_using=nx.DiGraph)
    else :
        return nx.from_pandas_edgelist(df, source=SENDER, target=RECIPIENT, create_using=nx.DiGraph)

def calculate_network_measures(G):
    """
    Calculate centrality measures for the undirected Graph G
    Add score of each measurement to the dataFrame

    :type G: networkx.dataFrame
    :rtype: networkx.dataFrame
    """
    in_degree = nx.in_degree_centrality(G) # a number of incoming links to a given node
    out_degree = nx.out_degree_centrality(G) # a number of outgoing links from a given node
    betweenness = nx.betweenness_centrality(G, weight=WEIGHT) # the frequency of a node appearing in shortest paths in the network
    closeness = nx.closeness_centrality(G, distance=WEIGHT) # the length of the shortest paths between the node and all other nodes in the graph
    eigenvector = nx.eigenvector_centrality(G.reverse(), weight=WEIGHT) # a relative measure of importance dependent on the importance of neighbouring nodes in the network
    clustering = nx.clustering(G.to_undirected(), weight=WEIGHT) # degree to which nodes in a graph tend to cluster together
    pagerank = nx.pagerank(G, weight=WEIGHT) # relative measure of importance also based on eigenvectors of an adjacency matrix
    max_clique = node_clique_number(G.to_undirected()) # size of the biggest clique for the specific node

    node_cliques = cliques_containing_node(G.to_undirected())
    node_cliques_count = {}
    for node, cliques in node_cliques.items():
        node_cliques_count[node] = len(cliques)

    network_df = pd.DataFrame(list(G.nodes), columns=[ID]);

    # add measure columns to dataFrame
    network_df[IN_DEGREE] = network_df[ID].map(in_degree)
    network_df[OUT_DEGREE] = network_df[ID].map(out_degree)
    network_df[BETWEENNESS] = network_df[ID].map(betweenness)
    network_df[CLOSENESS] = network_df[ID].map(closeness)
    network_df[EIGENVECTOR] = network_df[ID].map(eigenvector)
    network_df[CLUSTERING] = network_df[ID].map(clustering)
    network_df[PAGERANK] = network_df[ID].map(pagerank)
    network_df[MAX_CLIQUE] = network_df[ID].map(max_clique)
    network_df[CLIQUES_COUNT] = network_df[ID].map(node_cliques_count)

    return network_df
