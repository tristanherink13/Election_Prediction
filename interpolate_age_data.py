import os
import sys
import pandas as pd
import statistics

# read in 1980 age/sex data
df = pd.read_csv(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_sex_1980.csv'))

# initialize lists
state_list_65_69 = []
state_list_70_74 = []
state_list_75_79 = []
state_list_80_84 = []
state_list_85 = []
percent_65_69_list = []
percent_70_74_list = []
percent_75_79_list = []
percent_80_84_list = []
percent_85_list = []

# break up ages by age groups
group_1980 = df
code_list = group_1980['Code'].unique().tolist()

for code in code_list:
    state_list_65_69.append(group_1980.loc[(group_1980['Age'] >= 65)
    & (group_1980['Age'] <= 69) & (group_1980['Code'] == code), 'Both sexes'].sum())
    state_list_70_74.append(group_1980.loc[(group_1980['Age'] >= 70)
    & (group_1980['Age'] <= 74) & (group_1980['Code'] == code), 'Both sexes'].sum())
    state_list_75_79.append(group_1980.loc[(group_1980['Age'] >= 75)
    & (group_1980['Age'] <= 79) & (group_1980['Code'] == code), 'Both sexes'].sum())
    state_list_80_84.append(group_1980.loc[(group_1980['Age'] >= 80)
    & (group_1980['Age'] <= 84) & (group_1980['Code'] == code), 'Both sexes'].sum())
    state_list_85.append(group_1980.loc[(group_1980['Age'] >= 85)
    & (group_1980['Code'] == code), 'Both sexes'].sum())

for i, group in enumerate(state_list_65_69):
    total = group+state_list_70_74[i]+state_list_75_79[i]+state_list_80_84[i]+state_list_85[i]
    percent_65_69_list.append(round(state_list_65_69[i]/total, 2))
    percent_70_74_list.append(round(state_list_70_74[i]/total, 2))
    percent_75_79_list.append(round(state_list_75_79[i]/total, 2))
    percent_80_84_list.append(round(state_list_80_84[i]/total, 2))
    percent_85_list.append(round(state_list_85[i]/total, 2))

# calculate weighted average of age group population 
avg_65_69 = round(statistics.mean(percent_65_69_list), 2)
avg_70_74 = round(statistics.mean(percent_70_74_list), 2)
avg_75_79 = round(statistics.mean(percent_75_79_list), 2)
avg_80_84 = round(statistics.mean(percent_80_84_list), 2)
avg_85 = round(statistics.mean(percent_85_list), 2)