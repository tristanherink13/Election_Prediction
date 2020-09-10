import os
import sys

from election_data import ElectionData
from electoral_votes_data import ElectoralVotesData
from geopandas_data import GeopandasData
from overall_education_data import OverallEducationData
from rural_education_data import RuralEducationData
from urban_education_data import UrbanEducationData
from median_household_income_data import MedianHouseholdIncomeData
from demographic_data_1976 import DemographicData1976
from demographic_data_1980 import DemographicData1980

class Calculations():

    def __init__(self):
        # get ElectoralVotesData attributes
        self.electoral_votes = ElectoralVotesData()
        self.electoral_votes.read_data(os.path.join(sys.path[0], 'Datasets', 'electoral_votes_per_state.txt'))
        self.electoral_votes.convert_to_df()
        # get GeopandasData attributes
        self.geopandas = GeopandasData()
        self.geopandas.read_data(os.path.join(sys.path[0], 'Datasets', 'shapefile_mapping', 'cb_2018_us_state_500k.shp'))
        self.geopandas.convert_to_df()
        self.geopandas.manipulate_geopandas()
        self.usa = self.geopandas.gpd
        # get ElectionData attributes
        self.election_data_1976_2016 = ElectionData()
        self.election_data_1976_2016.read_data(os.path.join(sys.path[0], 'Datasets', 'election_data_1976_2016', '1976-2016-president.csv'))
        self.election_data_1976_2016.convert_to_df()
        self.election_data_1976_2016.manipulate_election_data()
        self.election_data_1976_2016.group_data()
        self.unique_abbrevs = self.election_data_1976_2016.df['STUSPS'].unique().tolist()
        # get OverallEducationData attributes
        self.overall_education = OverallEducationData()
        self.overall_education.read_data(os.path.join(sys.path[0], 'Datasets', 'college_complete_rural_urban_data', 'Overall_College_Complete_State.csv'))
        self.overall_education.convert_to_df()
        self.overall_education_df = self.overall_education.df
        # get RuralEducationData attributes
        self.rural_education = RuralEducationData()
        self.rural_education.read_data(os.path.join(sys.path[0], 'Datasets', 'college_complete_rural_urban_data', 'Rural_College_Complete_State.csv'))
        self.rural_education.convert_to_df()
        self.rural_education_df = self.rural_education.df
        # get UrbanEducationData attributes
        self.urban_education = UrbanEducationData()
        self.urban_education.read_data(os.path.join(sys.path[0], 'Datasets', 'college_complete_rural_urban_data', 'Urban_College_Complete_State.csv'))
        self.urban_education.convert_to_df()
        self.urban_education_df = self.urban_education.df
        # get MedianHouseholdIncomeData attributes
        self.income_data = MedianHouseholdIncomeData()
        self.income_data.read_data(os.path.join(sys.path[0], 'Datasets', 'median_household_income_data', 'median_household_income_1984_2018.csv'))
        self.income_data.convert_to_df()
        self.income_df = self.income_data.df
        # get DemographicData1976 attributes
        self.demographics_1976 = DemographicData1976()
        self.demographics_1976.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_1976.csv'))
        self.demographics_1976.convert_to_df()
        self.demographic_df_1976 = self.demographics_1976.df
        # get DemographicData1980 attributes
        self.demographics_1980 = DemographicData1980()
        self.demographics_1980.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_Sex_1980.csv'))
        self.demographics_1980.convert_to_df()
        self.demographic_df_1980 = self.demographics_1980.df

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