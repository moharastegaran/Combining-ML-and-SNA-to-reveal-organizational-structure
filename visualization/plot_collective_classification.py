import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from main.root_dir import data_root

from main.src.constants import *


class PlotCollectiveClassification:
    def __init__(self, levels, random_baseline):
        self.path = data_root()+r"\logs\collective_classification"
        self.levels = levels
        self.random_baseline = random_baseline
        self.colors = ['red', 'blue', 'black', '#2FBF71', '#FAA916']
        self.markers = ['D', 's', '<', 'o', 'X']
        self.linestyles = ['--', '-', '--', '-', '--']
        self.x_labels = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%']

    def plot(self):
        sns.set_style("darkgrid")
        sns.set_context("notebook")

        plt.figure(figsize=(10, 6))

        for month in MONTHS:
            df = pd.read_csv(self.path + r'\log_months_' + str(month) + '.csv', sep=';')
            result_series = df.groupby('pct')['f1_score'].max()
            result_series = result_series.sort_index()
            result_series.to_csv(self.path + r'\best_score_month_{0}.csv'.format(month), sep=';', index=True)
            plt.plot(self.x_labels, result_series.tolist(), label=str(month), linestyle=self.linestyles[month-1], marker=self.markers[month-1], color=self.colors[month-1])

        # random result is approximately 0.42 based on the results from random_classification.ipynb
        random_values = [self.random_baseline(self.levels)]*9
        plt.plot(self.x_labels, random_values, label='random', linestyle=':', marker='*', color='black')

        if self.levels == 2:
            levels_desc = 'two'
        else:
            levels_desc = 'three'

        plt.legend(loc='lower left', fontsize='small')
        plt.xlim(-1, 9)
        plt.ylim(0, 1.2)
        plt.xticks(np.arange(0,10))
        plt.xlabel('Known nodes')
        plt.ylabel('f1 score (macro)')
        plt.title('CollectiveClassification - ' + levels_desc + ' management levels')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., title='Minimum activity in months')
        plt.savefig(self.path + r'\collective_classification_' + str(self.levels) + '.eps', bbox_inches='tight', format='eps')
        plt.show()
