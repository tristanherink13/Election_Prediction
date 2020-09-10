import pandas as pd
import geopandas as gpd
import ast

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