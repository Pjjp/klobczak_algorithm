import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 


table_2 = pd.read_csv('2_column.csv')
table_3 = pd.read_csv('3_column.csv')

class Klobczak:
    def __init__(self, cube_size = 10000, tables = [], curent_element_count = []):
        self.cube_size = cube_size
        self.tables = tables
        self.curent_element_count = curent_element_count


    def split(self, table):
        split_axis = self.find_split_axis(table)
        element_count = table.A.count()

        #######################
        self.tables.append(table)
        self.curent_element_count.append(element_count)
        #######################

        if(element_count> self.cube_size):
            #print(element_count)
            #####################
            median = np.median(table[split_axis])
            split_table1 = table[table[split_axis] > median]
            split_table2 = table[table[split_axis] <= median]
            self.split(split_table1)
            self.split(split_table2)


    def find_split_axis(self, table):
        greatest_variance = 0
        for col in table.columns:
            variance = table[col].var()
            if(variance > greatest_variance): 
                greatest_variance = variance
                split_axis = col
        return split_axis

k = Klobczak(10000)
k.split(table_2)
print(k.curent_element_count[2])
print(k.tables[2])

for tab in k.tables:
