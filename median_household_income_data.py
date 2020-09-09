import pandas as pd
from dataset import Dataset

class MedianHouseholdIncomeData(Dataset):

    def read_income_data(self):
        # median household income per state and US overall (51x11)
        self.df = pd.read_csv(self.file_path)

    def group_data(self):
        # group by different attributes
        self.year_party_grouping = self.df.groupby(['year', 'party', 'STUSPS'])['candidatevotes'].sum()
        self.year_winner_grouping = self.df.groupby(['year', 'party', 'candidate'])['candidatevotes'].sum()
        self.all_popular_votes_df = self.df.groupby(['year', 'candidate'])['candidatevotes'].sum()