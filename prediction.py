from calculations import Calculations

import sys
import os
import pandas as pd

class Prediction(Calculations):
    
    def __init__(self):
        # get Calculations attributes
        prediction_data_object = Calculations()
        prediction_data_object.get_prediction_data()
        prediction_data_object.get_plotting_data()
        # education data
        self.overall_education_df = prediction_data_object.overall_education_df
        self.rural_education_df = prediction_data_object.rural_education_df
        self.urban_education_df = prediction_data_object.urban_education_df
        # income data
        self.income_df = prediction_data_object.income_df
        # demographic data
        self.demographic_df_1976 = prediction_data_object.demographic_df_1976
        self.demographic_df_1980 = prediction_data_object.demographic_df_1980
        self.demographic_df_1984 = prediction_data_object.demographic_df_1984
        self.demographic_df_1988 = prediction_data_object.demographic_df_1988
        self.demographic_df_1992 = prediction_data_object.demographic_df_1992
        self.demographic_df_1996 = prediction_data_object.demographic_df_1996
        self.demographic_df_2000 = prediction_data_object.demographic_df_2000
        self.demographic_df_2004 = prediction_data_object.demographic_df_2004
        self.demographic_df_2008 = prediction_data_object.demographic_df_2008
        self.demographic_df_2012 = prediction_data_object.demographic_df_2012
        self.demographic_df_2016 = prediction_data_object.demographic_df_2016
        self.demographic_df_2018 = prediction_data_object.demographic_df_2018
        # historical voting data
        self.rep_dem_state_df = pd.read_csv(os.path.join(sys.path[0], 'Datasets', 'election_data_1976_2016', 'dem_rep_state_votes.csv'))