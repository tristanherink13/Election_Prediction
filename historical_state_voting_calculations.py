import os
import sys
import pandas as pd

from calculations import Calculations
from election_data import ElectionData
from electoral_votes_data import ElectoralVotesData
from geopandas_data import GeopandasData

class HistoricalStateVotingCalculations(Calculations):
    
    def __init__(self):
        # get ElectoralVotesData attributes
        self.electoral_votes = ElectoralVotesData(os.path.join(sys.path[0], 'Datasets', 'electoral_votes_per_state.txt'))
        self.electoral_votes.open_txt_file()
        # get GeopandasData attributes
        self.geopandas = GeopandasData(os.path.join(sys.path[0], 'Datasets', 'shapefile_mapping', 'cb_2018_us_state_500k.shp'))
        self.geopandas.manipulate_geopandas()
        self.usa = self.geopandas.gpd
        # get ElectionData attributes
        self.election_data_1976_2016 = ElectionData(os.path.join(sys.path[0], 'Datasets', 'election_data_1976_2016', '1976-2016-president.csv'))
        self.election_data_1976_2016.manipulate_election_data()
        self.election_data_1976_2016.group_data()
        self.unique_abbrevs = self.election_data_1976_2016.df['STUSPS'].unique().tolist()
        # initialize attributes
        self.dem_states_won = 0
        self.rep_states_won = 0
        self.dem_state_percentage = 0
        self.rep_state_percentage = 0
        self.total_dem_electoral_votes = 0
        self.total_rep_electoral_votes = 0
        self.dem_candidate = ''
        self.rep_candidate = ''
        self.dem_pop_vote = 0
        self.rep_pop_vote = 0
        self.winner_ordered_list = []
        self.state_ordered_list = []
        self.electoral_votes_ordered_list = []
        self.winner_dict = {}
        self.alpha_ordered_states = []
        self.alpha_ordered_colors = []
        self.alpha_ordered_electoral_votes = []

        print('calculating winner per state and overall winner...')

    def determine_historical_winner(self, year):
        self.year = year
        # initialize local variables
        years = [1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016]
        dem_votes_per_state = []
        rep_votes_per_state = []
        dem_value_dict_list = []
        rep_value_dict_list = []
        dem_value_dict = {}
        rep_value_dict = {}
        winner_list = []
        winner_dict_list = []

        # get number of votes for each party/year/state
        year_party_grouping = self.election_data_1976_2016.year_party_grouping
        for yr in years:
            for state in self.unique_abbrevs:
                try:
                    dem_votes_per_state.append(year_party_grouping[yr]['democrat'][state])
                    rep_votes_per_state.append(year_party_grouping[yr]['republican'][state])
                except:
                    dem_votes_per_state.append(year_party_grouping[yr]['democratic-farmer-labor'][state])
                    rep_votes_per_state.append(year_party_grouping[yr]['republican'][state])
        
        # put key value pair of {state:count} in dict
        for i in range(0, len(dem_votes_per_state), 51):
            dem_value_dict = dict(zip(self.unique_abbrevs, dem_votes_per_state[i:i+51]))
            dem_value_dict_list.append(dem_value_dict)
            rep_value_dict = dict(zip(self.unique_abbrevs, rep_votes_per_state[i:i+51]))
            rep_value_dict_list.append(rep_value_dict)
        
        # structure == {year:{state:count}}
        dem_dict = dict(zip(years, dem_value_dict_list))
        rep_dict = dict(zip(years, rep_value_dict_list))

        # find winner of each state/year
        for yr in dem_dict:
            for state in dem_dict[yr]:
                if dem_dict[yr][state] > rep_dict[yr][state]:
                    winner_list.append('BLUE')
                elif dem_dict[yr][state] < rep_dict[yr][state]:
                    winner_list.append('RED')
                else:
                    winner_list.append('NONE')

        # put key value pair of {state:winner} in dict
        for i in range(0, len(winner_list), 51):
            self.winner_dict = dict(zip(self.unique_abbrevs, winner_list[i:i+51]))
            winner_dict_list.append(self.winner_dict)

        # structure == {year:{state:winner}}
        self.winner_dict = dict(zip(years, winner_dict_list))

        # index votes/state based on input year
        electoral_votes_per_state_per_year_dict = self.electoral_votes.electoral_votes_per_state_per_year_dict
        electoral_votes_per_state = electoral_votes_per_state_per_year_dict[self.year]

        # create winner series and group df to ascertain popular vote count for both parties
        winner_series = pd.Series(self.winner_dict[self.year])
        self.alpha_ordered_states = list(winner_series.index)
        self.alpha_ordered_colors = list(winner_series.values)

        # create dict and series for alphanumerically ordered states and votes
        electoral_dict = dict(zip(self.alpha_ordered_states, electoral_votes_per_state))
        votes_series = pd.Series(electoral_dict)
        self.alpha_ordered_electoral_votes = list(votes_series.values)

        # create ordered lists to merge into geopandas df
        [self.winner_ordered_list.append(winner) for abbrev in self.usa['STUSPS'] for state, winner in winner_series.items() if state == abbrev]
        [self.state_ordered_list.append(state) for abbrev in self.usa['STUSPS'] for state, winner in winner_series.items() if state == abbrev]
        [self.electoral_votes_ordered_list.append(votes) for abbrev in self.usa['STUSPS'] for state, votes in votes_series.items() if state == abbrev]

        # count up electoral votes for each state
        for i, state in enumerate(self.state_ordered_list):
            if self.winner_ordered_list[i] == 'BLUE':
                self.total_dem_electoral_votes += self.electoral_votes_ordered_list[i]
            else:
                self.total_rep_electoral_votes += self.electoral_votes_ordered_list[i]
        
        # calculate electoral vote breakdown
        total_electoral_votes = self.total_dem_electoral_votes + self.total_rep_electoral_votes
        self.dem_states_won = self.winner_ordered_list.count('BLUE')
        self.rep_states_won = self.winner_ordered_list.count('RED')
        self.dem_state_percentage = round(self.total_dem_electoral_votes/total_electoral_votes*100,2)
        self.rep_state_percentage = round(self.total_rep_electoral_votes/total_electoral_votes*100,2)

        # identify dem/rep candidates
        year_winner_grouping = self.election_data_1976_2016.year_winner_grouping
        dem_grouping = year_winner_grouping[self.year]['democrat']
        rep_grouping = year_winner_grouping[self.year]['republican']
        self.dem_candidate = dem_grouping.index[0]
        self.rep_candidate = rep_grouping.index[0]

        # identify dem/rep popular votes
        all_popular_votes_df = self.election_data_1976_2016.all_popular_votes_df
        self.dem_pop_vote = all_popular_votes_df[self.year][self.dem_candidate]
        self.rep_pop_vote = all_popular_votes_df[self.year][self.rep_candidate]