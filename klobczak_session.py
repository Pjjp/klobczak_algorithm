# coding: utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

table_2 = pd.read_csv('2_column.csv')
table_3 = pd.read_csv('3_column.csv')
table_1 = table_2['A']

sns.jointplot(x='A', y='B', data=table_2)

bins = [150, 180, 190, 200, 210, 220, 250]
table_2['B'].hist(bins=bins)
table_1.value_counts()
table_1.sort_values()
table_2['A'].var()
np.median(table_2['B'])