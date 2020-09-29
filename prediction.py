from calculations import Calculations

import sys
import os
import pandas as pd
import numpy as np
from numpy import array
from numpy import mean
from numpy import std
from numpy.core.umath_tests import inner1d
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
import csv
import _pickle

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
        self.final_prediction_df = prediction_data_object.final_prediction_df

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

    def impute_missing_data(self):
        # create prediction df
        prediction_df = self.all_prediction_df
        prediction_df = prediction_df[prediction_df.Sex != 0]
        prediction_df = prediction_df[prediction_df.Ethnic_Origin != 0]

        # average male/female breakdown to extrapolate data fields
        average_male_percent = .492
        average_female_percent = 1 - average_male_percent

        # fill NaN values with U and assign national averages to each row
        new_df = prediction_df.assign(Male_Population=prediction_df['Male_Population'].fillna('U'))
        new_df = new_df.assign(Female_Population=new_df['Female_Population'].fillna('U'))

        new_df = new_df.assign(
                        Male_Population=new_df.apply(
                        lambda row: int(round(row.Population*average_male_percent, 0))
                        if row.Male_Population == 'U' else row.Male_Population, axis=1))
        new_df = new_df.assign(
                        Female_Population=new_df.apply(
                        lambda row: int(round(row.Population*average_female_percent, 0))
                        if row.Female_Population == 'U' else row.Female_Population, axis=1))

        # get mode for each categorical feature
        race_sex_mode = new_df['Race_Sex'].mode()
        ethnic_origin_mode = new_df['Ethnic_Origin'].mode()
        sex_mode = new_df['Sex'].mode()
        race_mode = new_df['Race'].mode()

        # convert NaN values into mode
        new_df = new_df.assign(Race_Sex=new_df['Race_Sex'].fillna(race_sex_mode[0]))
        new_df = new_df.assign(Ethnic_Origin=new_df['Ethnic_Origin'].fillna(ethnic_origin_mode[0]))
        new_df = new_df.assign(Sex=new_df['Sex'].fillna(sex_mode[0]))
        new_df = new_df.assign(Race=new_df['Race'].fillna(race_mode[0]))

        # write final df to csv
        new_df.to_csv('final_cleaned_prediction_data.csv', index=False)

        # create 2020 prediction df using 2018 data
        #final_2020_prediction_df = new_df[new_df['Winner'].isnull()]
        #final_2020_prediction_df.to_csv('prediction_dataset_2020.csv', index=False)
    
    def compare_multiple_models(self):
        ### 0 == Dem (BLUE), 1 == Rep (RED)
        print('running models on dataset...')
        # import cleaned and imputed df, perform final conversions
        df = self.final_prediction_df
        # create dfs for running model
        final_df_data = df[df['Winner'].notnull()]
        prediction_df_2020 = df[df['Winner'].isnull()]
        #del prediction_df_2020['Winner']
        #del prediction_df_2020['Year']

        ### testing

        final_df_data = final_df_data[final_df_data.Year != 1976]
        final_df_data = final_df_data[final_df_data.Year != 1980]
        final_df_data = final_df_data[final_df_data.Year != 1984]
        #final_df_data = final_df_data[final_df_data.Year != 1988]
        #final_df_data = final_df_data[final_df_data.Year != 1992]
        #final_df_data = final_df_data[final_df_data.Year != 1996]
        #final_df_data = final_df_data[final_df_data.Year != 2000]
        #final_df_data = final_df_data[final_df_data.Year != 2004]
        #final_df_data = final_df_data[final_df_data.Year != 2008]
        #final_df_data = final_df_data[final_df_data.Year != 2012]


        final_df_answer = final_df_data['Winner']
        # create dictionary of all individual year data
        years = [1976, 1980, 1984, 1988, 1992, 1996,
            2000, 2004, 2008, 2012, 2016, 2020]
        test_dict = {}
        training_dict = {}
        for year in years:
            if year != 2020:
                test_dict[year] = final_df_data.loc[final_df_data['Year'] == year]
            else:
                test_dict[year] = prediction_df_2020
            training_dict[year] = final_df_data.loc[final_df_data['Year'] != year]
        del final_df_data['Winner']
        del final_df_data['Year']

        # separate df into training and test data
        x_train, x_test, y_train, self.y_test = train_test_split(final_df_data, final_df_answer, test_size=0.3, random_state=0)
        #x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.25, random_state=0) # 0.25 x 0.8 = 0.2
        
        # instantiate models
        lr = LogisticRegression()
        rf = RandomForestClassifier(max_depth=7, random_state=13)
        svc = make_pipeline(StandardScaler(),
                            LinearSVC(random_state=13,
                                      tol=1e-5,
                                      loss='squared_hinge',
                                      max_iter=100,
                                      fit_intercept=False))
                                      #class_weight='balanced'))

        sgd = SGDClassifier(max_iter=1000, tol=1e-3)
        knn = KNeighborsClassifier(n_neighbors=3)
        bayes = GaussianNB()

        # create varibles for looping through models and outputting results
        models = [svc]#[lr, rf, svc, sgd, knn, bayes]
        columns = ['Year', 'Logistic Regression', 'Random Forest', 'Support Vector Classification',
                   'Stochastic Gradient Descent', 'K-Nearest Neighbors', 'Naive Bayes']
        model_names = columns[1:]
        filename = 'Election_Accuracy_9_28.csv'
        counter = 0

        # create results output file
        with open(filename, 'w') as csvfile:   
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(columns)
        
        years = [2008, 2012, 2016]#, 2020]#[2008, 2012, 2016]
        # iterate through each individual model for each year
        for year in years:
            score_list = []
            score_list.append(year)
            y_train = training_dict[year]['Winner']
            del training_dict[year]['Winner']
            x_train = training_dict[year]
            y_test = test_dict[year]['Winner']
            del test_dict[year]['Winner']
            x_test = test_dict[year]

            for i, model in enumerate(models):
                model.fit(x_train, y_train)
                #predictions = model.predict(x_test)
                #predictions_2020 = model.predict(x_test)
                #pd.options.mode.chained_assignment = None
                #prediction_df_2020['Winner'] = predictions_2020
                #prediction_df_2020.to_csv('predictions.csv', index=False)
                counter += 1
                # Save model
                #with open('churn_classifier_{}_{}.pkl'.format(model, counter), 'wb') as fid:
                #    _pickle.dump(model, fid)
                #print('done fitting {} model'.format(model_names[i]))
                if year != 2020:
                    score = model.score(x_test, y_test)
                    score_list.append(round(score, 4))
                    print('{}, {} performance: {}'.format(year, model_names[i], round(score, 4)))
            
            if year != 2020:
                # write to results output file
                with open(filename, 'a') as csvfile:   
                    csvwriter = csv.writer(csvfile) 
                    csvwriter.writerow(score_list)

    def run_best_model(self):
        print('running optimal model on dataset...')
        # import cleaned and imputed df, perform final conversions
        df = self.final_prediction_df
        # create dfs for running model
        final_df_data = df[df['Winner'].notnull()]
        prediction_df_2020 = df[df['Winner'].isnull()]
        del prediction_df_2020['Winner']
        del prediction_df_2020['Year']
        final_df_answer = final_df_data['Winner']
        del final_df_data['Winner']
        del final_df_data['Year']

        # separate df into training and test data
        #x_train, x_test, y_train, self.y_test = train_test_split(final_df_data, final_df_answer, test_size=0.3, random_state=0)
        
        # instantiate model
        rf = RandomForestClassifier(max_depth=7, random_state=13)
        
        # fit model to training data, calculate score of test data, and predict 2020 election
        rf.fit(x_train, y_train)
        self.predictions = rf.predict(x_test)
        self.score = rf.score(x_test, self.y_test)
        predictions_2020 = rf.predict(prediction_df_2020)
        pd.options.mode.chained_assignment = None
        prediction_df_2020['Winner'] = predictions_2020
        prediction_df_2020.to_csv('predictions.csv', index=False)

    def plot_confusion_matrix(self):
        print('plotting confusion matrix...')
        # make seaborn confusion matrix
        cm = metrics.confusion_matrix(self.y_test, self.predictions)
        plt.figure(figsize=(9,9))
        sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r')
        plt.ylabel('Actual label')
        plt.xlabel('Predicted label')
        all_sample_title = 'Accuracy Score: {0}'.format(self.score)
        plt.title(all_sample_title, size = 15)
        plt.show()