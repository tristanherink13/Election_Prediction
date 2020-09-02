import os
import sys

from election_data import ElectionData
from electoral_votes_data import ElectoralVotesData
from geopandas_data import GeopandasData

class Calculations():

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