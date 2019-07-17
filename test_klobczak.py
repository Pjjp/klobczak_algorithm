from unittest import TestCase

import pytest

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

from klobczak_algorithm_obj4 import Klobczak


class KlobczakTestCase(TestCase):

    def setUp(self):
        table_2 = pd.read_csv('2_column.csv')
        table_3 = pd.read_csv('3_column.csv')
        table_4 = pd.read_csv('4_column.csv')

        self.k = Klobczak(10000)
        self.k.split(table_2)
    
    def test_is_size_ok(self):

        for item in self.k.tables:
            self.assertTrue(self.k.cube_size*0.5 < item.A.count() <= self.k.cube_size)