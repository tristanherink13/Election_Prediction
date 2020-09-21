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
        self.all_prediction_df = prediction_data_object.all_prediction_df

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
        df_1976.columns = ['Code', 'Overall_Edu', 'Rural_Edu', 'Urban_Edu', 'Median_Income', 
                           'Age_Group', 'Population', 'Winner']    
        # create 1980 df
        df_1980 = self.overall_education_df[['Code', 'Overall_Edu_1980']]
        df_1980 = df_1980.merge(self.rural_education_df[['Code', 'Rural_Edu_1980']], on='Code')
        df_1980 = df_1980.merge(self.urban_education_df[['Code', 'Urban_Edu_1980']], on='Code')
        df_1980 = df_1980.merge(self.income_df[['Code', '1980_Median_Income']], on='Code')
        df_1980 = df_1980.merge(self.demographic_df_1980[['Code', 'Age_Group_1980', 
                               'Both_Sexes_1980', 'Male_1980', 'Female_1980']], on='Code')
        df_1980 = df_1980.merge(votes_df_1980[['Code', 'Winner']], on='Code')
        df_1980.columns = ['Code', 'Overall_Edu', 'Rural_Edu', 'Urban_Edu', 'Median_Income', 
                           'Age_Group', 'Population', 'Male_Population', 'Female_Population', 'Winner']
        # create 1984 df
        df_1984 = self.overall_education_df[['Code', 'Overall_Edu_1984']]
        df_1984 = df_1984.merge(self.rural_education_df[['Code', 'Rural_Edu_1984']], on='Code')
        df_1984 = df_1984.merge(self.urban_education_df[['Code', 'Urban_Edu_1984']], on='Code')
        df_1984 = df_1984.merge(self.income_df[['Code', '1984_Median_Income']], on='Code')
        df_1984 = df_1984.merge(self.demographic_df_1984[['Code', 'Age_Group_1984', 
                               'Both_Sexes_1984', 'Male_1984', 'Female_1984']], on='Code')
        df_1984 = df_1984.merge(votes_df_1984[['Code', 'Winner']], on='Code')
        df_1984.columns = ['Code', 'Overall_Edu', 'Rural_Edu', 'Urban_Edu', 'Median_Income', 
                           'Age_Group', 'Population', 'Male_Population', 'Female_Population', 'Winner']
        # create 1988 df
        df_1988 = self.overall_education_df[['Code', 'Overall_Edu_1988']]
        df_1988 = df_1988.merge(self.rural_education_df[['Code', 'Rural_Edu_1988']], on='Code')
        df_1988 = df_1988.merge(self.urban_education_df[['Code', 'Urban_Edu_1988']], on='Code')
        df_1988 = df_1988.merge(self.income_df[['Code', '1988_Median_Income']], on='Code')
        df_1988 = df_1988.merge(self.demographic_df_1988[['Code', 'Age_Group_1988', 
                               'Both_Sexes_1988', 'Male_1988', 'Female_1988']], on='Code')
        df_1988 = df_1988.merge(votes_df_1988[['Code', 'Winner']], on='Code')
        df_1988.columns = ['Code', 'Overall_Edu', 'Rural_Edu', 'Urban_Edu', 'Median_Income', 
                           'Age_Group', 'Population', 'Male_Population', 'Female_Population', 'Winner']
        # create 1992 df
        df_1992 = self.overall_education_df[['Code', 'Overall_Edu_1992']]
        df_1992 = df_1992.merge(self.rural_education_df[['Code', 'Rural_Edu_1992']], on='Code')
        df_1992 = df_1992.merge(self.urban_education_df[['Code', 'Urban_Edu_1992']], on='Code')
        df_1992 = df_1992.merge(self.income_df[['Code', '1992_Median_Income']], on='Code')
        df_1992 = df_1992.merge(self.demographic_df_1992[['Code', 'Age_Group_1992', 
                               'Race_Sex_1992', 'Ethnic_Origin_1992', 'Population_1992']], on='Code')
        df_1992 = df_1992.merge(votes_df_1992[['Code', 'Winner']], on='Code')
        df_1992.columns = ['Code', 'Overall_Edu', 'Rural_Edu', 'Urban_Edu', 'Median_Income',
                           'Age_Group', 'Race_Sex', 'Ethnic_Origin', 'Population', 'Winner']
        
        # create 1996 df
        df_1996 = self.overall_education_df[['Code', 'Overall_Edu_1996']]
        df_1996 = df_1996.merge(self.rural_education_df[['Code', 'Rural_Edu_1996']], on='Code')
        df_1996 = df_1996.merge(self.urban_education_df[['Code', 'Urban_Edu_1996']], on='Code')
        df_1996 = df_1996.merge(self.income_df[['Code', '1996_Median_Income']], on='Code')
        df_1996 = df_1996.merge(self.demographic_df_1996[['Code', 'Age_Group_1996', 
                               'Race_Sex_1996', 'Ethnic_Origin_1996', 'Population_1996']], on='Code')
        df_1996 = df_1996.merge(votes_df_1996[['Code', 'Winner']], on='Code')
        df_1996.columns = ['Code', 'Overall_Edu', 'Rural_Edu', 'Urban_Edu', 'Median_Income',
                           'Age_Group', 'Race_Sex', 'Ethnic_Origin', 'Population', 'Winner']
        # create 2000 df
        df_2000 = self.overall_education_df[['Code', 'Overall_Edu_2000']]
        df_2000 = df_2000.merge(self.rural_education_df[['Code', 'Rural_Edu_2000']], on='Code')
        df_2000 = df_2000.merge(self.urban_education_df[['Code', 'Urban_Edu_2000']], on='Code')
        df_2000 = df_2000.merge(self.income_df[['Code', '2000_Median_Income']], on='Code')
        df_2000 = df_2000.merge(self.demographic_df_2000[['Code', 'Age_Group_2000', 
                               'SEX_2000', 'POPESTIMATE2000']], on='Code')
        df_2000 = df_2000.merge(votes_df_2000[['Code', 'Winner']], on='Code')
        df_2000.columns = ['Code', 'Overall_Edu', 'Rural_Edu', 'Urban_Edu', 'Median_Income',
                           'Age_Group', 'Sex', 'Population', 'Winner']
        # create 2004 df
        df_2004 = self.overall_education_df[['Code', 'Overall_Edu_2004']]
        df_2004 = df_2004.merge(self.rural_education_df[['Code', 'Rural_Edu_2004']], on='Code')
        df_2004 = df_2004.merge(self.urban_education_df[['Code', 'Urban_Edu_2004']], on='Code')
        df_2004 = df_2004.merge(self.income_df[['Code', '2004_Median_Income']], on='Code')
        df_2004 = df_2004.merge(self.demographic_df_2004[['Code', 'Age_Group_2004', 
                               'SEX_2004', 'POPESTIMATE2004']], on='Code')
        df_2004 = df_2004.merge(votes_df_2004[['Code', 'Winner']], on='Code')
        df_2004.columns = ['Code', 'Overall_Edu', 'Rural_Edu', 'Urban_Edu', 'Median_Income',
                           'Age_Group', 'Sex', 'Population', 'Winner']
        # create 2008 df
        df_2008 = self.overall_education_df[['Code', 'Overall_Edu_2008']]
        df_2008 = df_2008.merge(self.rural_education_df[['Code', 'Rural_Edu_2008']], on='Code')
        df_2008 = df_2008.merge(self.urban_education_df[['Code', 'Urban_Edu_2008']], on='Code')
        df_2008 = df_2008.merge(self.income_df[['Code', '2008_Median_Income']], on='Code')
        df_2008 = df_2008.merge(self.demographic_df_2008[['Code', 'Age_Group_2008', 
                               'SEX_2008', 'POPESTIMATE2008']], on='Code')
        df_2008 = df_2008.merge(votes_df_2008[['Code', 'Winner']], on='Code')
        df_2008.columns = ['Code', 'Overall_Edu', 'Rural_Edu', 'Urban_Edu', 'Median_Income',
                           'Age_Group', 'Sex', 'Population', 'Winner']
        # create 2012 df
        df_2012 = self.overall_education_df[['Code', 'Overall_Edu_2012']]
        df_2012 = df_2012.merge(self.rural_education_df[['Code', 'Rural_Edu_2012']], on='Code')
        df_2012 = df_2012.merge(self.urban_education_df[['Code', 'Urban_Edu_2012']], on='Code')
        df_2012 = df_2012.merge(self.income_df[['Code', '2012_Median_Income']], on='Code')
        os.path.join(sys.path[0], 'Datasets', 'college_complete_rural_urban_data', 'overall_college_complete_state.csv')
        df_2012 = df_2012.merge(self.demographic_df_2012[['Code', 'Age_Group_2012', 
                               'SEX_2012', 'ORIGIN_2012', 'RACE_2012', 'POPESTIMATE2012']], on='Code')
        df_2012 = df_2012.merge(votes_df_2012[['Code', 'Winner']], on='Code')
        df_2012.columns = ['Code', 'Overall_Edu', 'Rural_Edu', 'Urban_Edu', 'Median_Income',
                           'Age_Group', 'Sex', 'Ethnic_Origin', 'Race', 'Population', 'Winner']
        # create 2016 df
        df_2016 = self.overall_education_df[['Code', 'Overall_Edu_2016']]
        df_2016 = df_2016.merge(self.rural_education_df[['Code', 'Rural_Edu_2016']], on='Code')
        df_2016 = df_2016.merge(self.urban_education_df[['Code', 'Urban_Edu_2016']], on='Code')
        df_2016 = df_2016.merge(self.income_df[['Code', '2016_Median_Income']], on='Code')
        os.path.join(sys.path[0], 'Datasets', 'college_complete_rural_urban_data', 'overall_college_complete_state.csv')
        df_2016 = df_2016.merge(self.demographic_df_2016[['Code', 'Age_Group_2016', 
                               'SEX_2016', 'ORIGIN_2016', 'RACE_2016', 'POPESTIMATE2016']], on='Code')
        df_2016 = df_2016.merge(votes_df_2016[['Code', 'Winner']], on='Code')
        df_2016.columns = ['Code', 'Overall_Edu', 'Rural_Edu', 'Urban_Edu', 'Median_Income',
                           'Age_Group', 'Sex', 'Ethnic_Origin', 'Race', 'Population', 'Winner']
        # create 2018 df
        df_2018 = self.overall_education_df[['Code', 'Overall_Edu_2018']]
        df_2018 = df_2018.merge(self.rural_education_df[['Code', 'Rural_Edu_2018']], on='Code')
        df_2018 = df_2018.merge(self.urban_education_df[['Code', 'Urban_Edu_2018']], on='Code')
        df_2018 = df_2018.merge(self.income_df[['Code', '2018_Median_Income']], on='Code')
        os.path.join(sys.path[0], 'Datasets', 'college_complete_rural_urban_data', 'overall_college_complete_state.csv')
        df_2018 = df_2018.merge(self.demographic_df_2018[['Code', 'Age_Group_2018', 
                               'SEX_2018', 'ORIGIN_2018', 'RACE_2018', 'POPESTIMATE2018']], on='Code')
        df_2018.columns = ['Code', 'Overall_Edu', 'Rural_Edu', 'Urban_Edu', 'Median_Income',
                           'Age_Group', 'Sex', 'Ethnic_Origin', 'Race', 'Population']
        
        # concatenate all prediction data
        final_df = pd.concat([df_1976, df_1980, df_1984, df_1988, df_1992, df_1996, df_2000,
                              df_2004, df_2008, df_2012, df_2016, df_2018], axis=0, ignore_index=True)
        final_df.to_csv('all_prediction_data.csv', index=False)

    def run_model(self):
        print(self.all_prediction_df)