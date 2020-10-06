import pandas as pd
from dataset import Dataset

class DemographicData1980(Dataset):
    # age/sex data 1980 (4386x6)
    def bucketize_data(self, df):
        # initialize variables
        df = self.df
        code_list = df['Code'].unique().tolist()
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
                    group = df.loc[(df['Age_1980'] < age_range) & (df['Code'] == code),
                            ['Both_Sexes_1980', 'Male_1980', 'Female_1980']].sum()
                    group_list.append({code:{age_group_num_list[i]:group}})
                elif i == 18:
                    group = df.loc[(df['Age_1980'] >= age_range) & (df['Code'] == code),
                            ['Both_Sexes_1980', 'Male_1980', 'Female_1980']].sum()
                    group_list.append({code:{age_group_num_list[i]:group}})
                else:
                    group = df.loc[(df['Age_1980'] <= age_range[1]) & 
                            (df['Age_1980'] >= age_range[0]) & (df['Code'] == code),
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
        df_final.to_csv('demographic_buckets_1980.csv', index=False)
        self.df = df_final