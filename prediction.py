from calculations import Calculations

import sys
import os
import pandas as pd

class Prediction(Calculations):
    
    def __init__(self):
        # get Calculations attributes
        prediction_data_object = Calculations()
        prediction_data_object.get_prediction_data()
        # historical voting data
        self.dem_rep_state_df = prediction_data_object.dem_rep_votes_df
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

    def merge_prediction_data(self):
        dem_rep_df = self.dem_rep_state_df
        votes_df_1976 = dem_rep_df.loc[dem_rep_df['Year'] == 1976]
        votes_df_1980 = dem_rep_df.loc[dem_rep_df['Year'] == 1980]
        votes_df_1984 = dem_rep_df.loc[dem_rep_df['Year'] == 1984]
        votes_df_1988 = dem_rep_df.loc[dem_rep_df['Year'] == 1988]
        votes_df_1992 = dem_rep_df.loc[dem_rep_df['Year'] == 1992]
        votes_df_1996 = dem_rep_df.loc[dem_rep_df['Year'] == 1996]
        votes_df_2000 = dem_rep_df.loc[dem_rep_df['Year'] == 2000]
        votes_df_2004 = dem_rep_df.loc[dem_rep_df['Year'] == 2004]
        votes_df_2008 = dem_rep_df.loc[dem_rep_df['Year'] == 2008]
        votes_df_2012 = dem_rep_df.loc[dem_rep_df['Year'] == 2012]
        votes_df_2016 = dem_rep_df.loc[dem_rep_df['Year'] == 2016]

        # create 1976 df
        df_1976 = self.overall_education_df[['Code', 'Overall_Edu_1976']]
        df_1976 = df_1976.merge(self.rural_education_df[['Code', 'Rural_Edu_1976']], on='Code')
        df_1976 = df_1976.merge(self.urban_education_df[['Code', 'Urban_Edu_1976']], on='Code')
        df_1976 = df_1976.merge(self.income_df[['Code', '1976_Median_Income']], on='Code')
        df_1976 = df_1976.merge(self.demographic_df_1976[['Code', 'Age_Group_1976', 'Both_Sexes_1976']], on='Code')
        df_1976 = df_1976.merge(votes_df_1976[['Code', 'Winner']], on='Code')
        # create 1980 df
        df_1980 = self.overall_education_df[['Code', 'Overall_Edu_1980']]
        df_1980 = df_1980.merge(self.rural_education_df[['Code', 'Rural_Edu_1980']], on='Code')
        df_1980 = df_1980.merge(self.urban_education_df[['Code', 'Urban_Edu_1980']], on='Code')
        df_1980 = df_1980.merge(self.income_df[['Code', '1980_Median_Income']], on='Code')
        df_1980 = df_1980.merge(self.demographic_df_1980[['Code', 'Age_Group_1980', 
                               'Both_Sexes_1980', 'Male_1980', 'Female_1980']], on='Code')
        df_1980 = df_1980.merge(votes_df_1980[['Code', 'Winner']], on='Code')

        #####
        # df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
        #df_1976 = pd.concat([df_1976,df2], axis=0, ignore_index=True)
        #####