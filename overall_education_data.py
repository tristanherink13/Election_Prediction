import pandas as pd
from dataset import Dataset

class OverallEducationData(Dataset):

    def read_overall_education_data(self):
        # overall college complete (51x6)
        self.df = pd.read_csv(self.file_path)

    def group_data(self):
        # group by different attributes
        self.year_party_grouping = self.df.groupby(['year', 'party', 'STUSPS'])['candidatevotes'].sum()
        self.year_winner_grouping = self.df.groupby(['year', 'party', 'candidate'])['candidatevotes'].sum()
        self.all_popular_votes_df = self.df.groupby(['year', 'candidate'])['candidatevotes'].sum()