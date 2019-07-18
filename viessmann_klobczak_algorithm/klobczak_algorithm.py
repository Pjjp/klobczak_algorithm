import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

table_2 = pd.read_csv('2_column.csv')

def split(table):
    split_axis = find_split_axis(table)
    element_count = table.count().sum()

    if(element_count> 10000):
        median = np.median(table[split_axis])
        split_table1 = table[table[split_axis] > median]
        split_table2 = table[table[split_axis] <= median]
        split(split_table1)
        split(split_table2)


def find_split_axis(table):
    greatest_variance = 0
    for col in table.columns:
        variance = table[col].var()
        if(variance > greatest_variance): 
            greatest_variance = variance
            split_axis = col
    return split_axis

split(table_2)

