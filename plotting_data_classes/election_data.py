import pandas as pd
from dataset import Dataset

class ElectionData(Dataset):

    def manipulate_election_data(self):
        # drop writeins and irrelevant columns, and rename column to match other dataset for merging
        self.df = self.df[self.df.writein != True]
        self.df = self.df.drop(columns=['state_cen', 'version', 'notes', 'writein', 'state_ic', 'office'])
        self.df = self.df.rename(columns = {'state_po':'STUSPS'})

    def group_data(self):
        # group by different attributes
        self.year_party_grouping = self.df.groupby(['year', 'party', 'STUSPS'])['candidatevotes'].sum()
        self.year_winner_grouping = self.df.groupby(['year', 'party', 'candidate'])['candidatevotes'].sum()
        self.all_popular_votes_df = self.df.groupby(['year', 'candidate'])['candidatevotes'].sum()