import sys
import os
import ast
import pandas as pd
import geopandas as gpd

class Dataset:

    def read_data(self, file_path):
        self.file_path = file_path

    def convert_to_df(self):
        short_file_name = self.file_path.split('/')[-1]
        print('importing {} dataset...'.format(short_file_name))

        if short_file_name[-3:] == 'csv':
            self.df = pd.read_csv(self.file_path)
        elif short_file_name[-3:] == 'shp':
            self.gpd = gpd.read_file(self.file_path)
        elif short_file_name[-3:] == 'txt':
            with open(self.file_path, 'r') as data:
                self.electoral_votes_per_state_per_year_dict = ast.literal_eval(data.read())
    
    def drop_state_column(self, df):
        if 'State' in self.df.columns:
            self.df = self.df.drop(columns=['State'])

    '''
    def convert_acronyms_to_states(self, df):
        state_acro_df = pd.read_csv(os.path.join(sys.path[0], 'Datasets', 'state_acronym.csv'))
        state_list = state_acro_df['State'].tolist()
        acro_list = state_acro_df['Acronym'].tolist()
        code_list = state_acro_df['Code'].tolist()
        df_columns_list = []
        [df_columns_list.append(header.lower()) for header in self.df.columns.tolist()]

        # convert acronyms to state names
        for i, state in enumerate(state_list):
            self.df = self.df.replace(acro_list[i], state)
    '''