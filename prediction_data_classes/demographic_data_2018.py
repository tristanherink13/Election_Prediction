import pandas as pd
from dataset import Dataset

class DemographicData2018(Dataset):
    # age/race/sex 2018 per state (200k rows to 195k x 7)

    def bucketize_data(self, df):
        # initialize variables
        df = self.df
        df = df[df.CODE != 0]
        df = df[df.AGE_2018 != 999]
        code_list = df['CODE'].unique().tolist()
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
        sex_codes = [0, 1, 2]
        origin_codes = [0, 1, 2]
        race_codes = [1, 2, 3, 4, 5]

        # create dicts based on age range and code of grouped data
        for i, age_range in enumerate(age_range_list):
            for code in code_list:
                for sex in sex_codes:
                    for origin in origin_codes:
                        for race in race_codes:
                            if i == 0:
                                group = df.loc[(df['AGE_2018'] < age_range) & (df['CODE'] == code)
                                        & (df['SEX_2018'] == sex) & (df['ORIGIN_2018'] == origin)
                                        & (df['RACE_2018'] == race), ['POPESTIMATE2018']].sum()
                                group_list.append({code:{age_group_num_list[i]:group}})
                            elif i == 18:
                                group = df.loc[(df['AGE_2018'] >= age_range) & (df['CODE'] == code)
                                        & (df['SEX_2018'] == sex) & (df['ORIGIN_2018'] == origin)
                                        & (df['RACE_2018'] == race), ['POPESTIMATE2018']].sum()
                                group_list.append({code:{age_group_num_list[i]:group}})
                            else:
                                group = df.loc[(df['AGE_2018'] <= age_range[1])
                                        & (df['AGE_2018'] >= age_range[0]) & (df['CODE'] == code)
                                        & (df['SEX_2018'] == sex) & (df['ORIGIN_2018'] == origin)
                                        & (df['RACE_2018'] == race), ['POPESTIMATE2018']].sum()
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
            group.insert(1, 'Age_Group_2018', age_group_list[i], True)
            df_final = pd.concat([df_final, group], axis=0, ignore_index=True)
        # reorganize df, merge in other features, and assign to class
        df_final = df_final.sort_values(['Code', 'Age_Group_2018'], ascending=[True, True])
        df_final.to_csv('demographic_buckets_2018.csv', index=False)
        self.df = df_final