class Dataset:

    def __init__(self, file_path):
        self.file_path = file_path
        print('importing {} dataset...'.format(self.file_path.split('/')[-1]))
    
    def get_df_columns(self):
        self.df_columns = self.df.columns.to_list()
        return self.df_columns