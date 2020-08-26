### Presidential election data from 1976-2016

import os
import sys
import pandas as pd
import csv
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import time

class Dataset:
    """import data and create dataframe"""

    def __init__(self, file_path):
        print('importing dataset...')
        self.file_path = file_path

    def convert_to_df(self):
        df = pd.read_csv(self.file_path)
        return df

    def do_something(self):
        print(self.df)


file_path = os.path.join(sys.path[0], 'dataverse_files', '1976-2016-president.csv')
p_object = Dataset(file_path)

output = p_object.convert_to_df()

p_object.do_something

    # def main():
    #    """Main program loop"""
    #    print('yay its working!!')

#if __name__ == '__main__':
#    Dataset.main()