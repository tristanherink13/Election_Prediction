import os
import sys
import pandas as pd
from dataset import Dataset

class DemographicData1976(Dataset):
    # age data 1976 (1173x4)
    pass
    
    ### put this function in calculations class for each that needs converting
    def convert_states_to_acronyms(self):
        state_acro_df = pd.read_csv(os.path.join(sys.path[0], 'Datasets', 'state_acronym.csv'))
        state_list = state_acro_df['State'].tolist()
        acro_list = state_acro_df['Acronym'].tolist()
        for i, state in enumerate(state_list):
            self.df = self.df.replace(acro_list[i], state)
        return self.df