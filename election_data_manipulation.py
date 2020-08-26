### Presidential election data from 1976-2016

import os
import sys
import pandas as pd
import csv
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import time

# get file path
pd_file_path = os.path.join(sys.path[0], 'election_data_1976_2016', '1976-2016-president.csv')
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


def state_plotter(states, year, winner_dict, df, us_map=True):
# setting up us_map as an input. if you want to return states that are spred out, leave it set to true.
# if you're plotting bordering states and prefer to zoom in. 

    ### plot data on US map (https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)
    gpd_file_path = os.path.join(sys.path[0], 'shapefile_mapping', 'cb_2018_us_state_500k.shp')
    usa = gpd.read_file(gpd_file_path)

    # drop mappings (including Alaska + Hawaii for aesthetics)
    usa = usa[(usa.NAME != 'United States Virgin Islands') & (usa.NAME != 'Guam') 
            & (usa.NAME != 'Puerto Rico')& (usa.NAME != 'American Samoa')
            & (usa.NAME != 'Commonwealth of the Northern Mariana Islands')]

    # create winner series
    winner_series  = pd.Series(winner_dict[year])

    # create dicts for dem and rep nominees and extract relevant data
    
    
    year_winner_grouping = df.groupby(['year', 'party', 'candidate'])['candidatevotes'].sum()

    all_popular_votes_df = df.groupby(['year', 'candidate'])['candidatevotes'].sum()

    #year_winner_grouping[].nlargest(2)


    #print(year_winner_grouping[2000]['democrat'])


    #print(another_grouping[2000]['Gore, Al'])
    #final_usa['STUSPS'] == state

    #s = year_winner_grouping[2000]

    #print(s)

    #print(type(locate_person_df))

    dem_grouping = year_winner_grouping[year]['democrat']
    rep_grouping = year_winner_grouping[year]['republican']
    dem_candidate = dem_grouping.index[0]
    rep_candidate = rep_grouping.index[0]

    dem_pop_vote = all_popular_votes_df[year][dem_candidate]
    rep_pop_vote = all_popular_votes_df[year][rep_candidate]

    #dem_nom_dict = [dict(candidate=k, votes=v) for k, v in dem_grouping.items()]
    #rep_nom_dict = [dict(candidate=k, votes=v) for k, v in rep_grouping.items()]


    # create dict for num of electoral college votes/state/yr
    electoral_votes_per_state_per_year_dict = {
                                              1976:[9,3,6,6,45,7,8,3,3,17,12,4,4,26,13,
                                              8,7,9,10,4,10,14,21,10,7,12,4,5,3,4,17,
                                              4,41,13,3,25,8,6,27,4,8,4,10,26,4,3,12,
                                              9,6,11,3],
                                              1980:[9,3,6,6,45,7,8,3,3,17,12,4,4,26,13,
                                              8,7,9,10,4,10,14,21,10,7,12,4,5,3,4,17,4,
                                              41,13,3,25,8,6,27,4,8,4,10,26,4,3,12,9,6,
                                              11,3],
                                              1984:[9,3,7,6,47,8,8,3,3,21,12,4,4,24,12,
                                              8,7,9,10,4,10,13,20,10,7,11,4,5,4,4,16,5,
                                              36,13,3,23,8,7,25,4,8,3,11,29,5,3,12,10,
                                              6,11,3],
                                              1988: [9,3,7,6,47,8,8,3,3,21,12,4,4,24,12,
                                              8,7,9,10,4,10,13,20,10,7,11,4,5,4,4,16,5,
                                              36,13,3,23,8,7,25,4,8,3,11,29,5,3,12,10,
                                              6,11,3],
                                              1992: [9,3,8,6,54,8,8,3,3,25,13,4,4,22,12,
                                              7,6,8,9,4,10,12,18,10,7,11,3,5,4,4,15,5,
                                              33,14,3,21,8,7,23,4,8,3,11,32,5,3,13,11,
                                              5,11,3],
                                              1996: [9,3,8,6,54,8,8,3,3,25,13,4,4,22,12,
                                              7,6,8,9,4,10,12,18,10,7,11,3,5,4,4,15,5,
                                              33,14,3,21,8,7,23,4,8,3,11,32,5,3,13,11,
                                              5,11,3],
                                              2000: [9,3,8,6,54,8,8,3,3,25,13,4,4,22,12,
                                              7,6,8,9,4,10,12,18,10,7,11,3,5,4,4,15,5,
                                              33,14,3,21,8,7,23,4,8,3,11,32,5,3,13,11,
                                              5,11,3],
                                              2004: [9,3,10,6,55,9,7,3,3,27,15,4,4,21,11,
                                              7,6,8,9,4,10,12,17,10,6,11,3,5,5,4,15,5,31,
                                              15,3,20,7,7,21,4,8,3,11,34,5,3,13,11,5,10,3],
                                              2008: [9,3,10,6,55,9,7,3,3,27,15,4,4,21,11,
                                              7,6,8,9,4,10,12,17,10,6,11,3,5,5,4,15,5,31,
                                              15,3,20,7,7,21,4,8,3,11,34,5,3,13,11,5,10,3],
                                              2012: [9,3,11,6,55,9,7,3,3,29,16,4,4,20,11,
                                              6,6,8,8,4,10,11,16,10,6,10,3,5,6,4,14,5,29,
                                              15,3,18,7,7,20,4,9,3,11,38,6,3,13,12,5,10,3],
                                              2016: [9,3,11,6,55,9,7,3,3,29,16,4,4,20,11,
                                              6,6,8,8,4,10,11,16,10,6,10,3,5,6,4,14,5,29,
                                              15,3,18,7,7,20,4,9,3,11,38,6,3,13,12,5,10,3]
    }

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
    # to change size, use x_lim and y_lim. changing the figsize will not change the size of the map
    
    fig, ax = plt.subplots(figsize=(20,8))#, frameon=False)


    # Create a Rectangle patch
    rect = mpatches.Rectangle(
                             (1,1),30,40,linewidth=1,edgecolor='r',
                             fill=False,clip_on=False,clip_box=(.97, 1.01))#,
                             #zorder=2)#, set_bounds(left, bottom, width, height))
    
    #plt.legend(handles=[rect], title='Voting Statistics',loc='upper left')
    #ax.add_patch(rect)


    # shift states plot over to left
    ax = fig.add_axes([0.02, 0.02, 0.8, 0.8])

    # remove axis around map
    fig.subplots_adjust(wspace=0, top=1, right=1, left=0, bottom=0)

    ax.annotate(rect, (100,100), color='black', weight='bold', 
                fontsize=6, ha='center', va='center')

    # Add the patch to the Axes
    #ax2.add_patch(rect)

    ax.set_title('Presidential Winner By State, {}'.format(year), fontsize=14, x=.625)
    
    fortyeight = True
    xmin = -200
    xmax = -65
    ymin = 15
    ymax = 75


    
    
    #left = 10
    #bottom = 10
    #width = 10
    #height = 10
    #ax = fig.add_axes((left, bottom, width, height))
    
    
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

    if us_map:

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
    
        # the following loop will go through the list of input state abbreviations and plot them
        # ax=ax makes the states appear on the initial matplotlib figure
        for state in states:
            if fortyeight:
                if final_usa.loc[final_usa['STUSPS'] == state]['WINNER'].values[0] == 'BLUE': # tab20, tab20c, tab10
                    final_usa[final_usa.STUSPS == state].plot(ax=ax, color=rep_color, edgecolor='black', linewidth=line_thick).axis('off')#.tight_layout()
                elif final_usa.loc[final_usa['STUSPS'] == state]['WINNER'].values[0] == 'RED': # RdBu
                    final_usa[final_usa.STUSPS == state].plot(ax=ax, color=dem_color, edgecolor='black', linewidth=line_thick).axis('off')#.tight_layout()
            else:
                if usa.loc[usa['STUSPS'] == state]['WINNER'].values[0] == 'BLUE':
                    usa[usa.STUSPS == state].plot(ax=ax, color=rep_color, edgecolor='b', linewidth=line_thick)#, column='VOTES')
                elif usa.loc[usa['STUSPS'] == state]['WINNER'].values[0] == 'RED':
                    usa[usa.STUSPS == state].plot(ax=ax, color=dem_color, edgecolor='r', linewidth=line_thick)#, column='VOTES')

        plt.show()

    # if you choose not to have the first layer of the whole US, this will plot states on their own
    elif us_map == False:
        #final_usa = usa[(usa.STUSPS != 'AK') & (usa.STUSPS != 'HI')]
        final_usa = usa.drop(usa[usa.STUSPS == 'AK'])
        print(final_usa)
        #for state in states:
        #    if final_usa.loc[final_usa['STUSPS'] == state]['WINNER'].values[0] == 'BLUE':
        #        final_usa[final_usa.STUSPS == state].plot(ax=ax, cmap='plasma', edgecolor='b', linewidth=2, column='VOTES')
        #    elif final_usa.loc[final_usa['STUSPS'] == state]['WINNER'].values[0] == 'RED':
        #        final_usa[final_usa.STUSPS == state].plot(ax=ax, cmap='RdBu', edgecolor='r', linewidth=2, column='VOTES')
        #plt.show()

#state_plotter(['TX', 'CA', 'WA', 'VT'], 1976, winner_dict, df)
new_list = []
[new_list.append(st) for st in unique_abbrevs if st != 'AK' and st != 'HI']
state_plotter(new_list, 1984, winner_dict, df)#, us_map=False)
#state_plotter(unique_abbrevs, us_map = False)