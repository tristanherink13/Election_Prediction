import os
import sys
import pandas as pd

from ingest_datasets import ElectionData
from ingest_datasets import ElectoralVotesData
from ingest_datasets import GeopandasData

class Calculations():

    def __init__(self):
        pass

class StateVotingCalculations(Calculations):

    winner_ordered_list = []
    state_ordered_list = []
    electoral_votes_ordered_list = []
    
    def __init__(self):
        # get ElectoralVotesData attributes
        self.electoral_votes = ElectoralVotesData(os.path.join(sys.path[0], 'Datasets', 'electoral_votes_per_state.txt'))
        self.electoral_votes.open_txt_file()
        self.electoral_votes_per_state_per_year_dict = self.electoral_votes.electoral_votes_per_state_per_year_dict
        # get GeopandasData attributes
        self.geopandas = GeopandasData(os.path.join(sys.path[0], 'Datasets', 'shapefile_mapping', 'cb_2018_us_state_500k.shp'))
        self.geopandas.manipulate_geopandas()
        self.usa = self.geopandas.gpd
        # get ElectionData attributes
        self.election_data_1976_2016 = ElectionData(os.path.join(sys.path[0], 'Datasets', 'election_data_1976_2016', '1976-2016-president.csv'))
        self.election_data_1976_2016.manipulate_election_data()
        self.election_data_1976_2016.group_data()
        self.year_party_grouping = self.election_data_1976_2016.year_party_grouping
        self.year_winner_grouping = self.election_data_1976_2016.year_winner_grouping
        self.all_popular_votes_df = self.election_data_1976_2016.all_popular_votes_df
        self.unique_abbrevs = self.election_data_1976_2016.df['STUSPS'].unique().tolist()

        print('calculating winner per state and overall winner...')

    def determine_historical_winner(self, year):
        self.year = year
        self.years = [1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016]
        self.dem_votes_per_state = []
        self.rep_votes_per_state = []
        self.dem_value_dict_list = []
        self.rep_value_dict_list = []
        self.dem_value_dict = {}
        self.rep_value_dict = {}
        self.winner_list = []
        self.winner_dict_list = []
        self.winner_dict = {}

        # get number of votes for each party/year/state
        for year in self.years:
            for state in self.unique_abbrevs:
                try:
                    self.dem_votes_per_state.append(self.year_party_grouping[year]['democrat'][state])
                    self.rep_votes_per_state.append(self.year_party_grouping[year]['republican'][state])
                except:
                    self.dem_votes_per_state.append(self.year_party_grouping[year]['democratic-farmer-labor'][state])
                    self.rep_votes_per_state.append(self.year_party_grouping[year]['republican'][state])
        
        # put key value pair of {state:count} in dict
        for i in range(0, len(self.dem_votes_per_state), 51):
            self.dem_value_dict = dict(zip(self.unique_abbrevs, self.dem_votes_per_state[i:i+51]))
            self.dem_value_dict_list.append(self.dem_value_dict)
            self.rep_value_dict = dict(zip(self.unique_abbrevs, self.rep_votes_per_state[i:i+51]))
            self.rep_value_dict_list.append(self.rep_value_dict)
        
        # structure == {year:{state:count}}
        self.dem_dict = dict(zip(self.years, self.dem_value_dict_list))
        self.rep_dict = dict(zip(self.years, self.rep_value_dict_list))

        # find winner of each state/year
        for year in self.dem_dict:
            for state in self.dem_dict[year]:
                if self.dem_dict[year][state] > self.rep_dict[year][state]:
                    self.winner_list.append('BLUE')
                elif self.dem_dict[year][state] < self.rep_dict[year][state]:
                    self.winner_list.append('RED')
                else:
                    self.winner_list.append('NONE')

        # put key value pair of {state:winner} in dict
        for i in range(0, len(self.winner_list), 51):
            self.winner_dict = dict(zip(self.unique_abbrevs, self.winner_list[i:i+51]))
            self.winner_dict_list.append(self.winner_dict)

        # structure == {year:{state:winner}}
        self.winner_dict = dict(zip(self.years, self.winner_dict_list))

        # index votes/state based on input year
        self.electoral_votes_per_state = self.electoral_votes_per_state_per_year_dict[self.year]

        # create winner series and group df to ascertain popular vote count for both parties
        self.winner_series = pd.Series(self.winner_dict[self.year])

        # create dict and series for alphanumerically ordered states and votes
        self.alpha_ordered_states = list(self.winner_series.index)
        self.electoral_dict = dict(zip(self.alpha_ordered_states, self.electoral_votes_per_state))
        self.votes_series = pd.Series(self.electoral_dict)

        # create ordered lists to merge into geopandas df
        [self.winner_ordered_list.append(winner) for abbrev in self.usa['STUSPS'] for state, winner in self.winner_series.items() if state == abbrev]
        [self.state_ordered_list.append(state) for abbrev in self.usa['STUSPS'] for state, winner in self.winner_series.items() if state == abbrev]
        [self.electoral_votes_ordered_list.append(votes) for abbrev in self.usa['STUSPS'] for state, votes in self.votes_series.items() if state == abbrev]

        # count up electoral votes for each state
        self.total_dem_electoral_votes = 0
        self.total_rep_electoral_votes = 0
        for i, state in enumerate(self.state_ordered_list):
            if self.winner_ordered_list[i] == 'BLUE':
                self.total_dem_electoral_votes += self.electoral_votes_ordered_list[i]
            else:
                self.total_rep_electoral_votes += self.electoral_votes_ordered_list[i]
        
        # calculate electoral vote breakdown
        self.total_electoral_votes = self.total_dem_electoral_votes + self.total_rep_electoral_votes
        self.dem_states_won = self.winner_ordered_list.count('BLUE')
        self.rep_states_won = self.winner_ordered_list.count('RED')
        self.dem_state_percentage = round(self.total_dem_electoral_votes/self.total_electoral_votes*100,2)
        self.rep_state_percentage = round(self.total_rep_electoral_votes/self.total_electoral_votes*100,2)

        self.dem_grouping = self.year_winner_grouping[self.year]['democrat']
        self.rep_grouping = self.year_winner_grouping[self.year]['republican']
        self.dem_candidate = self.dem_grouping.index[0]
        self.rep_candidate = self.rep_grouping.index[0]

        self.dem_pop_vote = self.all_popular_votes_df[self.year][self.dem_candidate]
        self.rep_pop_vote = self.all_popular_votes_df[self.year][self.rep_candidate]