import ast
from dataset import Dataset

class ElectoralVotesData(Dataset):

    def open_txt_file(self):
        with open(self.file_path, 'r') as data:
            self.electoral_votes_per_state_per_year_dict = ast.literal_eval(data.read())