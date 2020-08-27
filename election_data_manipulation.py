### Presidential election data from 1976-2016

import os
import sys
import pandas as pd
import csv
import ast
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import time

# get file path
pd_file_path = os.path.join(sys.path[0], 'Datasets', 'election_data_1976_2016', '1976-2016-president.csv')
# read in CSV
df = pd.read_csv(pd_file_path)
# drop writeins
df = df[df.writein != True]
# drop irrelevant columns
df = df.drop(columns=['state_cen', 'version', 'notes', 'writein', 'state_ic', 'office'])

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

# get number of votes for each party/year/state
for year in years:
    for state in unique_abbrevs:
        try:
            dem_votes_per_state.append(year_party_grouping[year]['democrat'][state])
            rep_votes_per_state.append(year_party_grouping[year]['republican'][state])
        except:
            dem_votes_per_state.append(year_party_grouping[year]['democratic-farmer-labor'][state])
            rep_votes_per_state.append(year_party_grouping[year]['republican'][state])

# put key value pair of {state:count} in dict
for i in range(0, len(dem_votes_per_state), 51):
    dem_value_dict = dict(zip(unique_abbrevs, dem_votes_per_state[i:i+51]))
    dem_value_dict_list.append(dem_value_dict)
    rep_value_dict = dict(zip(unique_abbrevs, rep_votes_per_state[i:i+51]))
    rep_value_dict_list.append(rep_value_dict)

# structure == {year:{state:count}}
dem_dict = dict(zip(years, dem_value_dict_list))
rep_dict = dict(zip(years, rep_value_dict_list))

# find winner of each state/year
for year in dem_dict:
    for state in dem_dict[year]:
        if dem_dict[year][state] > rep_dict[year][state]:
            winner_list.append('BLUE')
        elif dem_dict[year][state] < rep_dict[year][state]:
            winner_list.append('RED')
        else:
            winner_list.append('NONE')

# put key value pair of {state:winner} in dict
for i in range(0, len(winner_list), 51):
    winner_dict = dict(zip(unique_abbrevs, winner_list[i:i+51]))
    winner_dict_list.append(winner_dict)

# structure == {year:{state:winner}}
winner_dict = dict(zip(years, winner_dict_list))

def state_plotter(states, year, winner_dict, df):

    ### plot data on US map (https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)
    gpd_file_path = os.path.join(sys.path[0],'Datasets', 'shapefile_mapping', 'cb_2018_us_state_500k.shp')
    usa = gpd.read_file(gpd_file_path)

    # drop irrelevant mappings
    usa = usa[(usa.NAME != 'United States Virgin Islands') & (usa.NAME != 'Guam') 
            & (usa.NAME != 'Puerto Rico')& (usa.NAME != 'American Samoa')
            & (usa.NAME != 'Commonwealth of the Northern Mariana Islands')]

    # create winner series and group df to ascertain popular vote count for both parties
    winner_series  = pd.Series(winner_dict[year])
    
    year_winner_grouping = df.groupby(['year', 'party', 'candidate'])['candidatevotes'].sum()
    all_popular_votes_df = df.groupby(['year', 'candidate'])['candidatevotes'].sum()

    dem_grouping = year_winner_grouping[year]['democrat']
    rep_grouping = year_winner_grouping[year]['republican']
    dem_candidate = dem_grouping.index[0]
    rep_candidate = rep_grouping.index[0]

    dem_pop_vote = all_popular_votes_df[year][dem_candidate]
    rep_pop_vote = all_popular_votes_df[year][rep_candidate]

    # read in dict with electoral votes per state per year
    electoral_path = os.path.join(sys.path[0], 'Datasets', 'electoral_votes_per_state.txt')
    with open(electoral_path, 'r') as data:
        electoral_votes_per_state_per_year_dict = ast.literal_eval(data.read())

    # index votes/state based on input year
    electoral_votes_per_state = electoral_votes_per_state_per_year_dict[year]

    # create dict and series for alphanumerically ordered states and votes
    alpha_ordered_states = list(winner_series.index)
    electoral_dict = dict(zip(alpha_ordered_states, electoral_votes_per_state))
    votes_series = pd.Series(electoral_dict)

    # create ordered lists to merge into geopandas df
    winner_ordered_list = []
    state_ordered_list = []
    electoral_votes_ordered_list = []
    [winner_ordered_list.append(winner) for abbrev in usa['STUSPS'] for state, winner in winner_series.items() if state == abbrev]
    [state_ordered_list.append(state) for abbrev in usa['STUSPS'] for state, winner in winner_series.items() if state == abbrev]
    [electoral_votes_ordered_list.append(votes) for abbrev in usa['STUSPS'] for state, votes in votes_series.items() if state == abbrev]

    # append winner and electoral votes data to geopandas df
    usa['WINNER'] = winner_ordered_list
    usa['VOTES'] = electoral_votes_ordered_list

    # instantiate a matplotlib figure
    fig, ax = plt.subplots(figsize=(20,8))

    # shift states plot over to left
    ax = fig.add_axes([0.02, 0.02, 0.8, 0.8])

    # remove axis around map
    fig.subplots_adjust(wspace=0, top=1, right=1, left=0, bottom=0)

    ax.set_title('Presidential Winner By State, {}'.format(year), fontsize=14, x=.625)
    
    fortyeight = True
    xmin = -200
    xmax = -65
    ymin = 15
    ymax = 75

    handles, labels = ax.get_legend_handles_labels()

    # choose color scheme and line thickness for dem/rep
    dem_color = '#3A34DB'
    rep_color = '#DC2C2C'
    line_thick = 1

    # start creating labels for legends
    legend_list = []
    total_dem_electoral_votes = 0
    total_rep_electoral_votes = 0
    for i, state in enumerate(state_ordered_list):
        if winner_ordered_list[i] == 'BLUE':
            legend = mpatches.Patch(color=dem_color, label='{} : {}'.format(state, electoral_votes_ordered_list[i]))
            total_dem_electoral_votes += electoral_votes_ordered_list[i]
        else:
            legend = mpatches.Patch(color=rep_color, label='{} : {}'.format(state, electoral_votes_ordered_list[i]))
            total_rep_electoral_votes += electoral_votes_ordered_list[i]
        legend_list.append(legend)

    # add label for running candidates and popular votes
    if total_dem_electoral_votes > total_rep_electoral_votes:
        win_legend = mpatches.Patch(color=dem_color, label=dem_candidate)
    else:
        win_legend = mpatches.Patch(color=rep_color, label=rep_candidate)

    if dem_pop_vote > rep_pop_vote:
        popular_win_legend = mpatches.Patch(color=dem_color, label='{} : {}'.format(dem_candidate, dem_pop_vote))
        popular_lose_legend = mpatches.Patch(color=rep_color, label='{} : {}'.format(rep_candidate, rep_pop_vote))
    else:
        popular_win_legend = mpatches.Patch(color=rep_color, label='{} : {}'.format(rep_candidate, rep_pop_vote))
        popular_lose_legend = mpatches.Patch(color=dem_color, label='{} : {}'.format(dem_candidate, dem_pop_vote))

    # calculate electoral vote breakdown
    total_electoral_votes = total_dem_electoral_votes + total_rep_electoral_votes
    dem_states_won = winner_ordered_list.count('BLUE')
    rep_states_won = winner_ordered_list.count('RED')
    dem_state_percentage = round(total_dem_electoral_votes/total_electoral_votes*100,2)
    rep_state_percentage = round(total_rep_electoral_votes/total_electoral_votes*100,2)

    # create legend for electoral vote breakdown
    dem_legend = mpatches.Patch(color=dem_color, label='{} votes ({}%)'.format(total_dem_electoral_votes, dem_state_percentage))
    dem_state_legend = mpatches.Patch(color=dem_color, label='{} states won'.format(dem_states_won))
    rep_legend = mpatches.Patch(color=rep_color, label='{} votes ({}%)'.format(total_rep_electoral_votes, rep_state_percentage))
    rep_state_legend = mpatches.Patch(color=rep_color, label='{} states won'.format(rep_states_won))

    # create legend for voting statistics by state
    if dem_states_won > rep_states_won:
        third_legend = [dem_legend, dem_state_legend, rep_legend, rep_state_legend]
    else:
        third_legend = [rep_legend, rep_state_legend, dem_legend, dem_state_legend]

    # plot legends
    first_legend = plt.legend(
                             handles=[win_legend], title='Winner', bbox_to_anchor=(.97, 1.01),
                             loc='upper left', fontsize='small', shadow=True
                             )

    first_pt_2_legend = plt.legend(
                             handles=[popular_win_legend, popular_lose_legend], 
                             title='Candidate : Popular Vote', bbox_to_anchor=(.97, .925),
                             loc='upper left', fontsize='small', shadow=True
                             )

    second_legend = plt.legend(
                              handles=legend_list, title='Electoral Votes', bbox_to_anchor=(.97, .815),
                              loc='upper left', fontsize='small', shadow=True, ncol=3
                              )

    plt.legend(
              handles=third_legend, title='Voting Statistics', bbox_to_anchor=(.97, .3),
              loc='upper left', fontsize='small', shadow=True
              )
    
    # Add overwritten legends manually
    ax.add_artist(first_legend)
    ax.add_artist(first_pt_2_legend)
    ax.add_artist(second_legend)

    # the following series of if/elif/else statements provide control over
    # whether Alaska and Hawaii will show up in the map. Because of their 
    # distance from the lower 48, and the size of Alaska, we don't want them
    # in the map unless necessary

    if 'AK' and 'HI' in states:
        fortyeight = False
        ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
    elif 'AK' in states:
        final_usa = usa[usa.STUSPS != 'HI']
        ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
    elif 'HI' in states:
        final_usa = usa[usa.STUSPS != 'AK']
    else:
        final_usa = usa[(usa.STUSPS != 'AK') & (usa.STUSPS != 'HI')]

    # go through the list of input state abbreviations and plot them
    for state in states:
        if fortyeight:
            if final_usa.loc[final_usa['STUSPS'] == state]['WINNER'].values[0] == 'BLUE':
                final_usa[final_usa.STUSPS == state].plot(ax=ax, color=rep_color, edgecolor='black', linewidth=line_thick).axis('off')
            elif final_usa.loc[final_usa['STUSPS'] == state]['WINNER'].values[0] == 'RED':
                final_usa[final_usa.STUSPS == state].plot(ax=ax, color=dem_color, edgecolor='black', linewidth=line_thick).axis('off')
        else:
            if usa.loc[usa['STUSPS'] == state]['WINNER'].values[0] == 'BLUE':
                usa[usa.STUSPS == state].plot(ax=ax, color=rep_color, edgecolor='b', linewidth=line_thick)
            elif usa.loc[usa['STUSPS'] == state]['WINNER'].values[0] == 'RED':
                usa[usa.STUSPS == state].plot(ax=ax, color=dem_color, edgecolor='r', linewidth=line_thick)

    plt.show()

#state_plotter(['TX', 'CA', 'WA', 'VT'], 1976, winner_dict, df)
main_states_list = []
[main_states_list.append(st) for st in unique_abbrevs if st != 'AK' and st != 'HI']
state_plotter(main_states_list, 1976, winner_dict, df)