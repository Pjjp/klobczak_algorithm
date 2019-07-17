import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import seaborn as sns 


table_2 = pd.read_csv('2_column.csv')
table_3 = pd.read_csv('3_column.csv')
table_4 = pd.read_csv('4_column.csv')

class Klobczak:
    def __init__(self, cube_size = 10000, tables = [], p_table = []):
        self.cube_size = cube_size
        self.tables = tables
        self.p_table = p_table


    def split(self, table):
        split_axis = self.find_split_axis(table)
        element_count = table[split_axis].count()

        median = np.median(table[split_axis])
        split_table1 = table[table[split_axis] > median]
        split_table2 = table[table[split_axis] < median]

        table_median = table.loc[table[split_axis] == median]
        half_of_all = table[split_axis].count()/2

        if(split_table1[split_axis].count()!=split_table2[split_axis].count()):
            split_table1 = split_table1.append( 
                table_median.head( int(half_of_all - split_table1[split_axis].count())) )
            split_table2 = split_table2.append( 
                table_median.tail( int(half_of_all - split_table2[split_axis].count())) )

        if(element_count> self.cube_size):
            self.split(split_table1)
            self.split(split_table2)
        else:
            self.tables.append(table)


    def find_split_axis(self, table):
        greatest_variance = 0
        for col in table.columns:
            variance = table[col].var()
            if(variance > greatest_variance): 
                greatest_variance = variance
                split_axis = col
        return split_axis


    def draw_2d(self):
        x_min = self.p_table.A.min()
        x_max = self.p_table.A.max()
        y_min = self.p_table.B.min()
        y_max = self.p_table.B.max()

        fig, ax = plt.subplots()
        for tab in self.tables:
            ax.add_artist(mpatch.Rectangle((tab.A.min(), tab.B.min()), 
                                         tab.A.max()-tab.A.min(), tab.B.max()-tab.B.min(), fill = None))
        ax.set_xlim((x_min, x_max))
        ax.set_ylim((y_min, y_max))
        plt.show()