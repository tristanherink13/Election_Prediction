import geopandas as gpd
from dataset import Dataset

class GeopandasData(Dataset):

    def manipulate_geopandas(self):
        # drop irrelevant mappings
        self.gpd = self.gpd[(self.gpd.NAME != 'United States Virgin Islands') & (self.gpd.NAME != 'Guam') 
                          & (self.gpd.NAME != 'Puerto Rico')& (self.gpd.NAME != 'American Samoa')
                          & (self.gpd.NAME != 'Commonwealth of the Northern Mariana Islands')]