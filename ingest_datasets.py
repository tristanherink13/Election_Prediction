import pandas as pd
import ast
import geopandas as gpd

class Dataset:

    def __init__(self, file_path):
        self.file_path = file_path
        print('importing {} dataset...'.format(self.file_path.split('/')[-1]))
    
    def get_df_columns(self):
        self.df_columns = self.df.columns.to_list()
        return self.df_columns
    
class ElectionData(Dataset):

    def manipulate_election_data(self):
        # convert to df, drop writeins and irrelevant columns, and rename column to match other dataset for merging
        self.df = pd.read_csv(self.file_path)
        self.df = self.df[self.df.writein != True]
        self.df = self.df.drop(columns=['state_cen', 'version', 'notes', 'writein', 'state_ic', 'office'])
        self.df = self.df.rename(columns = {'state_po':'STUSPS'})

    def group_data(self):
        # group by different attributes
        self.year_party_grouping = self.df.groupby(['year', 'party', 'STUSPS'])['candidatevotes'].sum()
        self.year_winner_grouping = self.df.groupby(['year', 'party', 'candidate'])['candidatevotes'].sum()
        self.all_popular_votes_df = self.df.groupby(['year', 'candidate'])['candidatevotes'].sum()

class GeopandasData(Dataset):

    def manipulate_geopandas(self):
        self.gpd = gpd.read_file(self.file_path)
        # drop irrelevant mappings
        self.gpd = self.gpd[(self.gpd.NAME != 'United States Virgin Islands') & (self.gpd.NAME != 'Guam') 
                          & (self.gpd.NAME != 'Puerto Rico')& (self.gpd.NAME != 'American Samoa')
                          & (self.gpd.NAME != 'Commonwealth of the Northern Mariana Islands')]

class ElectoralVotesData(Dataset):

    def open_txt_file(self):
        with open(self.file_path, 'r') as data:
            self.electoral_votes_per_state_per_year_dict = ast.literal_eval(data.read())