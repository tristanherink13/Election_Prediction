import os
import sys
import pandas as pd
import statistics

# read in 1980 age/sex data
df = pd.read_csv(os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'age_sex_1980.csv'))

# initialize lists for calculating interpolation averages
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

# initialize variables
group_1980 = df
code_list = group_1980['Code'].unique().tolist()
df_final = pd.DataFrame()
group_list = []
inside_group_list = []
code_key_list = []
final_group_list = []
age_group_list = []
age_range_list = [(1), (1,4), (5,9), (10,14), (15,19), (20,24), (25,29), (30,34),
                  (35,39), (40,44), (45,49), (50,54), (55,59), (60,64), (65,69),
                  (70,74), (75,79), (80,84), (85)]
age_group_num_list = list(range(0, 19))

# create dicts based on age range and code of grouped data
for i, age_range in enumerate(age_range_list):
    for code in code_list:
        if i == 0:
            group = group_1980.loc[(group_1980['Age_1980'] < age_range) & (group_1980['Code'] == code),
                    ['Both_Sexes_1980', 'Male_1980', 'Female_1980']].sum()
            group_list.append({code:{age_group_num_list[i]:group}})
        elif i == 18:
            group = group_1980.loc[(group_1980['Age_1980'] >= age_range) & (group_1980['Code'] == code),
                    ['Both_Sexes_1980', 'Male_1980', 'Female_1980']].sum()
            group_list.append({code:{age_group_num_list[i]:group}})
        else:
            group = group_1980.loc[(group_1980['Age_1980'] <= age_range[1]) & 
                    (group_1980['Age_1980'] >= age_range[0]) & (group_1980['Code'] == code),
                    ['Both_Sexes_1980', 'Male_1980', 'Female_1980']].sum()
            group_list.append({code:{age_group_num_list[i]:group}})

# create lists of states codes and {age_group:values}
for group in group_list:
    for key, value in group.items():
        inside_group_list.append(group[key])
        code_key_list.append(key)
# create lists of age groups and values
for group in inside_group_list:
    for k, v in group.items():
        final_group_list.append(group[k])
        age_group_list.append(k)
# manipulate all group series to conform to df for merging later on
for i, group in enumerate(final_group_list):
    group = group.to_frame().T
    group.insert(0, 'Code', code_key_list[i], True)
    group.insert(1, 'Age_Group_1980', age_group_list[i], True)
    df_final = pd.concat([df_final, group], axis=0, ignore_index=True)
# reorganize df and assign to class
df_final = df_final.sort_values(['Code', 'Age_Group_1980'], ascending=[True, True])



# calculate averages for population interpolation
for code in code_list:
    state_list_65_69.append(group_1980.loc[(group_1980['Age_1980'] >= 65)
    & (group_1980['Age_1980'] <= 69) & (group_1980['Code'] == code), 'Both_Sexes_1980'].sum())
    state_list_70_74.append(group_1980.loc[(group_1980['Age_1980'] >= 70)
    & (group_1980['Age_1980'] <= 74) & (group_1980['Code'] == code), 'Both_Sexes_1980'].sum())
    state_list_75_79.append(group_1980.loc[(group_1980['Age_1980'] >= 75)
    & (group_1980['Age_1980'] <= 79) & (group_1980['Code'] == code), 'Both_Sexes_1980'].sum())
    state_list_80_84.append(group_1980.loc[(group_1980['Age_1980'] >= 80)
    & (group_1980['Age_1980'] <= 84) & (group_1980['Code'] == code), 'Both_Sexes_1980'].sum())
    state_list_85.append(group_1980.loc[(group_1980['Age_1980'] >= 85)
    & (group_1980['Code'] == code), 'Both_Sexes_1980'].sum())

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