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
            if 'prediction_data' in short_file_name:
                self.df = pd.read_csv(self.file_path, encoding = 'ISO-8859-1', dtype=object)
            elif 'acronym' in short_file_name or 'predictions' in short_file_name:
                self.df = pd.read_csv(self.file_path)
            else:
                self.df = pd.read_csv(self.file_path, encoding = 'ISO-8859-1')
        elif short_file_name[-3:] == 'shp':
            self.gpd = gpd.read_file(self.file_path)
        elif short_file_name[-3:] == 'txt':
            with open(self.file_path, 'r') as data:
                if 'electoral' in short_file_name:
                    self.electoral_votes_per_state_per_year_dict = ast.literal_eval(data.read())
                else:
                    self.probable_outcomes_538_dict = ast.literal_eval(data.read())
    
    def drop_state_column(self, df):
        if 'State' in self.df.columns:
            self.df = self.df.drop(columns=['State'])
    
    def drop_senate_house_cols(self, df):
        # initialize all state codes and years
        codes = [1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,
                25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,
                45,46,47,48,49,50,51,53,54,55,56]
        years = [1976, 1978, 1980, 1982, 1984, 1986, 1988,
                 1992, 1996, 1998, 2000, 2002, 2004, 2006,
                 2008, 2010, 2012, 2014, 2016, 2018]
        # drop unneccesary columns
        self.df = self.df.drop(columns=['state_cen', 'state_ic', 'district', 'stage', 'special',
                                        'candidate', 'writein', 'mode', 'unofficial', 'version',
                                        'state', 'state_po', 'office'])
        # iterate through and fill in states with no senate/house votes for a specific year
        for year in years:
            year_df = self.df[self.df['Year'] == year]
            df_code_list = year_df['Code'].unique()
            for code in codes:
                if code not in df_code_list:
                    self.df.loc[-1] = [year, code, 'nothing', 0, 0]
                    self.df.index = self.df.index + 1
                    self.df = self.df.sort_index()
        # re-map dem/rep/other to 0/1/2
        if 'sen_party' in self.df.columns:
            self.df['sen_party'] = self.df['sen_party'].map({'democrat': 0, 'republican': 1})
            self.df['sen_party'] = self.df['sen_party'].fillna(2)
            self.df = self.df.groupby(['sen_party', 'Year', 'Code'])[['sen_candidatevotes', 'sen_totalvotes']].sum().reset_index()
        elif 'house_party' in self.df.columns:
            self.df['house_party'] = self.df['house_party'].map({'democrat': 0, 'republican': 1})
            self.df['house_party'] = self.df['house_party'].fillna(2)
            self.df = self.df.groupby(['house_party', 'Year', 'Code'])[['house_candidatevotes', 'house_totalvotes']].sum().reset_index()