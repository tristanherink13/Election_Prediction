import pandas as pd
import os
import sys

# overall college complete (51x6)
file_path = os.path.join(sys.path[0], 'Datasets', 'college_complete_rural_urban_data', 'Overall_College_Complete_State.csv')
df = pd.read_csv(file_path)

# rural college complete (51x6)
file_path = os.path.join(sys.path[0], 'Datasets', 'college_complete_rural_urban_data', 'Rural_College_Complete_State.csv')
df = pd.read_csv(file_path)

# urban college complete (51x6)
file_path = os.path.join(sys.path[0], 'Datasets', 'college_complete_rural_urban_data', 'Urban_College_Complete_State.csv')
df = pd.read_csv(file_path)

# median household income per state and US overall (51x11)
file_path = os.path.join(sys.path[0], 'Datasets', 'median_household_income_data', 'median_household_income_1984_2018.csv')
df = pd.read_csv(file_path)

# age data 1976 (1173x4)
file_path = os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_1976.csv')
df = pd.read_csv(file_path)

# age/sex data 1980 (4386x6)
file_path = os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_Sex_1980.csv')
df = pd.read_csv(file_path)

# age/sex data 1984 (4386x6)
file_path = os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_Sex_1984.csv')
df = pd.read_csv(file_path)

# age/sex data 1988 (4386x6)
file_path = os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_Sex_1988.csv')
df = pd.read_csv(file_path)

# age/race/sex data 1992 (950k rows down to 475k x 5)
file_path = os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_Race_Sex_1992.csv')
df = pd.read_csv(file_path)

# age/race/sex data 1996 (950k rows down to 480k x 5)
file_path = os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_Race_Sex_1996.csv')
df = pd.read_csv(file_path)

# age/sex data 2000 per state and US overall (13572x5)
file_path = os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_Sex_2000.csv')
df = pd.read_csv(file_path)

# age/sex data 2004 per state and US overall (13572x5)
file_path = os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_Sex_2004.csv')
df = pd.read_csv(file_path)

# age/sex data 2008 per state and US overall (13572x5)
file_path = os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_Sex_2008.csv')
df = pd.read_csv(file_path)

# age/race/sex 2012 per state (200k rows down to 194k x 7)
file_path = os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_Race_Sex_2012.csv')
df = pd.read_csv(file_path)

# age/race/sex 2016 per state (200k rows down to 195k x 7)
file_path = os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_Race_Sex_2016.csv')
df = pd.read_csv(file_path)

# age/race/sex 2018 per state (200k rows down to 195k x 7)
file_path = os.path.join(sys.path[0], 'Datasets', 'population_race_sex_data', 'Age_Race_Sex_2018.csv')
df = pd.read_csv(file_path)