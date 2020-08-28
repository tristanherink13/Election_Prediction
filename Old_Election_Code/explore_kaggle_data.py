import os
import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import svm

### going to first start with Linear SVC bc we're predicting a category based on a <100k labeled dataset (108 columns)

class Dataset:
    def __init__(self, file_path):
        self.file_path = file_path
        print('importing {} dataset...'.format(self.file_path.split('/')[-1]))

    def convert_to_df(self):
        self.df = pd.read_csv(self.file_path)
        return self.df
    
    def get_df_columns(self):
        self.df_columns = self.df.columns.to_list()
        return self.df_columns

# instantiate objects
test_object = Dataset(os.path.join(sys.path[0], 'Datasets', 'kaggle_2016_dataset', 'test2016.csv'))
train_object = Dataset(os.path.join(sys.path[0], 'Datasets', 'kaggle_2016_dataset', 'train2016.csv'))

# convert object to df
test_df = test_object.convert_to_df()
train_df = train_object.convert_to_df()

# get column headers of df
test_columns = test_object.get_df_columns()
train_columns = train_object.get_df_columns()