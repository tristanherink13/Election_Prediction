import os
import sys

from election_data import ElectionData
from electoral_votes_data import ElectoralVotesData
from geopandas_data import GeopandasData
from dem_rep_state_votes_data import DemRepStateVotesData
from overall_education_data import OverallEducationData
from rural_education_data import RuralEducationData
from urban_education_data import UrbanEducationData
from median_household_income_data import MedianHouseholdIncomeData
from demographic_data_1976 import DemographicData1976
from demographic_data_1980 import DemographicData1980
from demographic_data_1984 import DemographicData1984
from demographic_data_1988 import DemographicData1988
from demographic_data_1992 import DemographicData1992
from demographic_data_1996 import DemographicData1996
from demographic_data_2000 import DemographicData2000
from demographic_data_2004 import DemographicData2004
from demographic_data_2008 import DemographicData2008
from demographic_data_2012 import DemographicData2012
from demographic_data_2016 import DemographicData2016
from demographic_data_2018 import DemographicData2018

class Calculations():

    def __init__(self):
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

    def get_plotting_data(self):
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
    
    def get_prediction_data(self):
        # get DemRepStateVotesData attributes
        self.dem_rep_votes_data = DemRepStateVotesData()
        self.dem_rep_votes_data.read_data(os.path.join(sys.path[0], 'Datasets', 'election_data_1976_2016', 'dem_rep_state_votes.csv'))
        self.dem_rep_votes_data.convert_to_df()
        self.dem_rep_votes_data.drop_state_column(self.dem_rep_votes_data.df)
        self.dem_rep_votes_df = self.dem_rep_votes_data.df
        # get OverallEducationData attributes
        self.overall_education = OverallEducationData()
        self.overall_education.read_data(os.path.join(sys.path[0], 'Datasets', 'college_complete_rural_urban_data', 'overall_college_complete_state.csv'))
        self.overall_education.convert_to_df()
        self.overall_education.drop_state_column(self.overall_education.df)
        self.overall_education_df = self.overall_education.df
        # get RuralEducationData attributes
        self.rural_education = RuralEducationData()
        self.rural_education.read_data(os.path.join(sys.path[0], 'Datasets', 'college_complete_rural_urban_data', 'rural_college_complete_state.csv'))
        self.rural_education.convert_to_df()
        self.rural_education.drop_state_column(self.rural_education.df)
        self.rural_education_df = self.rural_education.df
        # get UrbanEducationData attributes
        self.urban_education = UrbanEducationData()
        self.urban_education.read_data(os.path.join(sys.path[0], 'Datasets', 'college_complete_rural_urban_data', 'urban_college_complete_state.csv'))
        self.urban_education.convert_to_df()
        self.urban_education.drop_state_column(self.urban_education.df)
        self.urban_education_df = self.urban_education.df
        # get MedianHouseholdIncomeData attributes
        self.income_data = MedianHouseholdIncomeData()
        self.income_data.read_data(os.path.join(sys.path[0], 'Datasets', 'median_household_income_data', 'median_household_income_1976_2018.csv'))
        self.income_data.convert_to_df()
        self.income_data.drop_state_column(self.income_data.df)
        self.income_df = self.income_data.df
        # get DemographicData1976 attributes
        self.demographics_1976 = DemographicData1976()
        self.demographics_1976.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_1976.csv'))
        self.demographics_1976.convert_to_df()
        self.demographics_1976.drop_state_column(self.demographics_1976.df)
        self.demographics_1976.bucketize_data(self.demographics_1976.df)
        self.demographic_df_1976 = self.demographics_1976.df
        # get DemographicData1980 attributes
        self.demographics_1980 = DemographicData1980()
        self.demographics_1980.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_sex_1980.csv'))
        self.demographics_1980.convert_to_df()
        self.demographics_1980.drop_state_column(self.demographics_1980.df)
        self.demographics_1980.bucketize_data(self.demographics_1980.df)
        self.demographic_df_1980 = self.demographics_1980.df
        # get DemographicData1984 attributes
        self.demographics_1984 = DemographicData1984()
        self.demographics_1984.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_sex_1984.csv'))
        self.demographics_1984.convert_to_df()
        self.demographics_1984.drop_state_column(self.demographics_1984.df)
        self.demographic_df_1984 = self.demographics_1984.df
        # get DemographicData1988 attributes
        self.demographics_1988 = DemographicData1988()
        self.demographics_1988.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_sex_1988.csv'))
        self.demographics_1988.convert_to_df()
        self.demographics_1988.drop_state_column(self.demographics_1988.df)
        self.demographic_df_1988 = self.demographics_1988.df
        # get DemographicData1992 attributes
        self.demographics_1992 = DemographicData1992()
        self.demographics_1992.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_race_sex_1992.csv'))
        self.demographics_1992.convert_to_df()
        self.demographic_df_1992 = self.demographics_1992.df
        # get DemographicData1996 attributes
        self.demographics_1996 = DemographicData1996()
        self.demographics_1996.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_race_sex_1996.csv'))
        self.demographics_1996.convert_to_df()
        self.demographic_df_1996 = self.demographics_1996.df
        # get DemographicData2000 attributes
        self.demographics_2000 = DemographicData2000()
        self.demographics_2000.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_sex_2000.csv'))
        self.demographics_2000.convert_to_df()
        self.demographics_2000.drop_state_column(self.demographics_2000.df)
        self.demographic_df_2000 = self.demographics_2000.df
        # get DemographicData2004 attributes
        self.demographics_2004 = DemographicData2004()
        self.demographics_2004.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_sex_2004.csv'))
        self.demographics_2004.convert_to_df()
        self.demographics_2004.drop_state_column(self.demographics_2004.df)
        self.demographic_df_2004 = self.demographics_2004.df
        # get DemographicData2008 attributes
        self.demographics_2008 = DemographicData2008()
        self.demographics_2008.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_sex_2008.csv'))
        self.demographics_2008.convert_to_df()
        self.demographics_2008.drop_state_column(self.demographics_2008.df)
        self.demographic_df_2008 = self.demographics_2008.df
        # get DemographicData2012 attributes
        self.demographics_2012 = DemographicData2012()
        self.demographics_2012.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_race_sex_2012.csv'))
        self.demographics_2012.convert_to_df()
        self.demographics_2012.drop_state_column(self.demographics_2012.df)
        self.demographic_df_2012 = self.demographics_2012.df
        # get DemographicData2016 attributes
        self.demographics_2016 = DemographicData2016()
        self.demographics_2016.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_race_sex_2016.csv'))
        self.demographics_2016.convert_to_df()
        self.demographics_2016.drop_state_column(self.demographics_2016.df)
        self.demographic_df_2016 = self.demographics_2016.df
        # get DemographicData2018 attributes
        self.demographics_2018 = DemographicData2018()
        self.demographics_2018.read_data(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_race_sex_2018.csv'))
        self.demographics_2018.convert_to_df()
        self.demographics_2018.drop_state_column(self.demographics_2018.df)
        self.demographic_df_2018 = self.demographics_2018.df