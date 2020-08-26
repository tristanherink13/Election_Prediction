### Presidential election data from 1976-2016

import os
import pandas as pd
import csv
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import matplotlib
import time

### clean up data
# get file path
file_path = os.getcwd()
# read in CSV
df = pd.read_csv(file_path+'/dataverse_files/1976-2016-president.csv')
# drop writeins
df = df[df.writein != True]
# drop irrelevant columns
df = df.drop(columns=['state_cen', 'version', 'notes', 'writein', 'state_ic', 'office'])

### plot data on US map (https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)
usa = gpd.read_file(file_path+'/cb_2018_us_state_500k/cb_2018_us_state_500k.shp')

# drop mappings (including Alaska + Hawaii for aesthetics)
usa = usa[(usa.NAME != 'United States Virgin Islands') & (usa.NAME != 'Guam') 
           & (usa.NAME != 'Puerto Rico')& (usa.NAME != 'American Samoa')
           & (usa.NAME != 'Commonwealth of the Northern Mariana Islands')]

# rename column to match with other dataframe for merging later on
df = df.rename(columns = {'state_po':'STUSPS'})
unique_states = df['state'].unique().tolist()
unique_abbrevs = df['STUSPS'].unique().tolist()


# group by year, party, and state abbreviation
year_party_grouping = df.groupby(['year', 'party', 'STUSPS'])['candidatevotes'].sum()

# initialize lists
years = [1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016]
dem_votes_per_state = []
rep_votes_per_state = []
dem_value_dict_list = []
rep_value_dict_list = []
dem_value_dict = {}
rep_value_dict = {}
winner_list = []
winner_dict_list = []
winner_dict = {}

# get number of votes for each party per year per state
for year in years:
    for state in unique_abbrevs:
        try:
            dem_votes_per_state.append(year_party_grouping[year]['democrat'][state])
            rep_votes_per_state.append(year_party_grouping[year]['republican'][state])
        except:
            dem_votes_per_state.append(0)
            rep_votes_per_state.append(0)

# put key value pair of {state:count} in dict
for i in range(0, len(dem_votes_per_state), 51):
    dem_value_dict = dict(zip(unique_abbrevs, dem_votes_per_state[i:i+51]))
    dem_value_dict_list.append(dem_value_dict)
    rep_value_dict = dict(zip(unique_abbrevs, rep_votes_per_state[i:i+51]))
    rep_value_dict_list.append(rep_value_dict)

# structure == {year:{state:count}}
dem_dict = dict(zip(years, dem_value_dict_list))
rep_dict = dict(zip(years, rep_value_dict_list))

# find winner of each state per year
for year in dem_dict:
    for state in dem_dict[year]:
        if dem_dict[year][state] > rep_dict[year][state]:
            winner_list.append('BLUE')
            #print('Democrats won {} in {}!'.format(state, year))
        elif dem_dict[year][state] < rep_dict[year][state]:
            winner_list.append('RED')
            #print('Republicans won {} in {}!'.format(state, year))
        else:
            winner_list.append('NONE')
            #print('Neither party won {} in {}'.format(state, year))


# put key value pair of {state:winner} in dict
for i in range(0, len(winner_list), 51):
    winner_dict = dict(zip(unique_abbrevs, winner_list[i:i+51]))
    winner_dict_list.append(winner_dict)

# structure == {year:{state:winner}}
winner_dict = dict(zip(years, winner_dict_list))


def state_plotter(states, year, winner_dict, us_map=True):
# setting up us_map as an input. if you want to return states that are spred out, leave it set to true.
# if you're plotting bordering states and prefer to zoom in. 

    # create winner df
    s  = pd.Series(winner_dict[year])
    winner_df = pd.DataFrame({'STUSPS':s.index, 'WINNER':s.values})

    gdf = gpd.read_file("tc_line.shp")
    gdf["pi"]= 1
    gdf.to_file("tc_pi.shp") 

    # merge winner df with usa df
    merged_df = pd.merge(winner_df, usa, on='STUSPS', how='inner')

    #result = merged_df.loc[merged_df['STUSPS'] == 'TX']['WINNER'].values[0]

    # instantiate a matplotlib figure
    # to change size, use x_lim and y_lim. changing the figsize will not change the size of the map
    
    fig, ax = plt.subplots(figsize=(20,8))
    fortyeight = False
    xmin = -200
    xmax = -65
    ymin = 15
    ymax = 75

    #ax.set_xlabel('x-label', fontsize=12)
    #ax.set_ylabel('y-label', fontsize=12)
    ax.set_title('States', fontsize=12)

    if us_map:

    # the following series of if/elif/else statements provide control over
    # whether Alaska and Hawaii will show up in the map. Because of their 
    # distance from the lower 48, and the size of Alaska, we don't want them
    # in the map unless necessary

        if 'AK' and 'HI' in states:
            fortyeight = True
            ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        elif 'AK' in states:
            final_usa = usa[usa.STUSPS != 'HI']
            ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        elif 'HI' in states:
            final_usa = usa[usa.STUSPS != 'AK']
        else:
            final_usa = usa[(usa.STUSPS != 'AK') & (usa.STUSPS != 'HI')]
    
    # the following loop will go through the list of input state abbreviations and plot them
    # ax=ax makes the states appear on the initial matplotlib figure
        for state in states:
            if not fortyeight:
                final_usa[final_usa.STUSPS == state].plot(ax=ax, edgecolor='y', linewidth=2)
            else:
                usa[usa.STUSPS == state].plot(ax=ax, edgecolor='y', linewidth=2)
        plt.show()

    # if you choose not to have the first layer of the whole US, this will plot states on their own
    elif us_map == False:
        for state in states:
            usa[usa.STUSPS == state].plot(ax=ax, edgecolor='y', linewidth=2)
        plt.show()

state_plotter(['TX', 'CA', 'WA', 'VT', 'HI', 'AK'], 1976, winner_dict)
#state_plotter(unique_abbrevs, us_map = False)

#usa.plot(ax=ax, legend=True)
#usa.plot(cmap='OrRd')
#plt.show()
#plt.tight_layout()