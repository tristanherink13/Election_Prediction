from dataset import Dataset

class DemographicData1976(Dataset):
    # age data 1976 (1173x4 to 969x4 after combining)
    def bucketize_data(self, df):
        df = self.df
        df['freq'] = df.groupby(['Code', 'Age_Group_1976'])['Age_Group_1976'].transform('count')
        keep_df = df[df.freq < 2]
        drop_df = df[df.freq > 1]
        del keep_df['freq']
        sum_series = drop_df.groupby(['Code', 'Age_Group_1976'])['Both_Sexes_1976'].sum()
        sum_df = sum_series.to_frame().reset_index()
        keep_df = keep_df.append(sum_df, ignore_index = True)
        keep_df = keep_df.sort_values(['Code', 'Age_Group_1976'], ascending=[True, True])
        keep_df.to_csv('demographic_buckets_1976.csv', index=False)
        self.df = keep_df