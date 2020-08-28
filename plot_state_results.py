import pandas as pd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib

from ingest_datasets import ElectionData
from perform_calculations import StateVotingCalculations

class StatePlotter:

    main_states_list = []

    def __init__(self, year):
        self.year = year
        # get StateVotingCalculations attributes
        self.calculations = StateVotingCalculations()
        self.winner_method = self.calculations.determine_historical_winner(self.year)
        self.winner_dict = self.calculations.winner_dict
        self.unique_abbrevs = self.calculations.unique_abbrevs
        [self.main_states_list.append(st) for st in self.unique_abbrevs if st != 'AK' and st != 'HI']
        self.dem_pop_vote = self.calculations.dem_pop_vote
        self.rep_pop_vote = self.calculations.rep_pop_vote
        self.rep_candidate = self.calculations.rep_candidate
        self.dem_candidate = self.calculations.dem_candidate
        self.winner_ordered_list = self.calculations.winner_ordered_list
        self.state_ordered_list = self.calculations.state_ordered_list
        self.electoral_votes_ordered_list = self.calculations.electoral_votes_ordered_list
        self.total_dem_electoral_votes = self.calculations.total_dem_electoral_votes
        self.total_rep_electoral_votes = self.calculations.total_rep_electoral_votes
        self.total_electoral_votes = self.calculations.total_electoral_votes
        self.dem_states_won = self.calculations.dem_states_won
        self.rep_states_won = self.calculations.rep_states_won
        self.dem_state_percentage = self.calculations.dem_state_percentage
        self.rep_state_percentage = self.calculations.rep_state_percentage
        self.usa = self.calculations.usa

        print('plotting data...')

class PlotHistoricalData(StatePlotter):

    legend_list = []

    def merge_historical_data_into_gpd(self):
        # append winner and electoral votes data to geopandas df
        self.usa['WINNER'] = self.winner_ordered_list
        self.usa['VOTES'] = self.electoral_votes_ordered_list
    
    def create_figure(self):
        # initialize variables
        self.fortyeight = True
        self.xmin = -200
        self.xmax = -65
        self.ymin = 15
        self.ymax = 75
        # instantiate a matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(20,8))
        # shift states plot over to left
        self.ax = self.fig.add_axes([0.02, 0.02, 0.8, 0.8])
        # remove axis around map
        self.fig.subplots_adjust(wspace=0, top=1, right=1, left=0, bottom=0)
        # set title
        self.ax.set_title('Presidential Winner By State, {}'.format(self.year), fontsize=14, x=.625)
        # choose color scheme and line thickness for dem/rep
        self.dem_color = '#3A34DB'
        self.rep_color = '#DC2C2C'
        self.line_thick = 1

        # start creating labels for legends
        self.handles, self.labels = self.ax.get_legend_handles_labels()

        # label each state red/blue and count up electoral votes
        for i, state in enumerate(self.state_ordered_list):
            if self.winner_ordered_list[i] == 'BLUE':
                self.legend = mpatches.Patch(color=self.dem_color, label='{} : {}'.format(state, self.electoral_votes_ordered_list[i]))
            else:
                self.legend = mpatches.Patch(color=self.rep_color, label='{} : {}'.format(state, self.electoral_votes_ordered_list[i]))
            self.legend_list.append(self.legend)
        
        # add label for running candidates and popular votes
        if self.total_dem_electoral_votes > self.total_rep_electoral_votes:
            self.win_legend = mpatches.Patch(color=self.dem_color, label=self.dem_candidate)
        else:
            self.win_legend = mpatches.Patch(color=self.rep_color, label=self.rep_candidate)

        if self.dem_pop_vote > self.rep_pop_vote:
            self.popular_win_legend = mpatches.Patch(color=self.dem_color, label='{} : {}'.format(self.dem_candidate, self.dem_pop_vote))
            self.popular_lose_legend = mpatches.Patch(color=self.rep_color, label='{} : {}'.format(self.rep_candidate, self.rep_pop_vote))
        else:
            self.popular_win_legend = mpatches.Patch(color=self.rep_color, label='{} : {}'.format(self.rep_candidate, self.rep_pop_vote))
            self.popular_lose_legend = mpatches.Patch(color=self.dem_color, label='{} : {}'.format(self.dem_candidate, self.dem_pop_vote))

        # create legend for electoral vote breakdown
        self.dem_legend = mpatches.Patch(color=self.dem_color, label='{} votes ({}%)'.format(self.total_dem_electoral_votes, self.dem_state_percentage))
        self.dem_state_legend = mpatches.Patch(color=self.dem_color, label='{} states won'.format(self.dem_states_won))
        self.rep_legend = mpatches.Patch(color=self.rep_color, label='{} votes ({}%)'.format(self.total_rep_electoral_votes, self.rep_state_percentage))
        self.rep_state_legend = mpatches.Patch(color=self.rep_color, label='{} states won'.format(self.rep_states_won))

        # create legend for voting statistics by state
        if self.dem_states_won > self.rep_states_won:
            self.third_legend = [self.dem_legend, self.dem_state_legend, self.rep_legend, self.rep_state_legend]
        else:
            self.third_legend = [self.rep_legend, self.rep_state_legend, self.dem_legend, self.dem_state_legend]
        
        # plot legends
        self.first_legend = plt.legend(
                                handles=[self.win_legend], title='Winner', bbox_to_anchor=(.97, 1.01),
                                loc='upper left', fontsize='small', shadow=True
                                )

        self.first_pt_2_legend = plt.legend(
                                handles=[self.popular_win_legend, self.popular_lose_legend], 
                                title='Candidate : Popular Vote', bbox_to_anchor=(.97, .925),
                                loc='upper left', fontsize='small', shadow=True
                                )

        self.second_legend = plt.legend(
                                handles=self.legend_list, title='Electoral Votes', bbox_to_anchor=(.97, .815),
                                loc='upper left', fontsize='small', shadow=True, ncol=3
                                )

        plt.legend(
                handles=self.third_legend, title='Voting Statistics', bbox_to_anchor=(.97, .3),
                loc='upper left', fontsize='small', shadow=True
                )

        # Add overwritten legends manually
        self.ax.add_artist(self.first_legend)
        self.ax.add_artist(self.first_pt_2_legend)
        self.ax.add_artist(self.second_legend)

        # the following series of if/elif/else statements provide control over
        # whether Alaska and Hawaii will show up in the map. Because of their 
        # distance from the lower 48, and the size of Alaska, we don't want them
        # in the map unless necessary

        if 'AK' and 'HI' in self.main_states_list:
            self.fortyeight = False
            self.ax.set(xlim=(self.xmin, self.xmax), ylim=(self.ymin, self.ymax))
        elif 'AK' in self.main_states_list:
            self.final_usa = self.usa[self.usa.STUSPS != 'HI']
            self.ax.set(xlim=(self.xmin, self.xmax), ylim=(self.ymin, self.ymax))
        elif 'HI' in self.main_states_list:
            self.final_usa = self.usa[self.usa.STUSPS != 'AK']
        else:
            self.final_usa = self.usa[(self.usa.STUSPS != 'AK') & (self.usa.STUSPS != 'HI')]

        # go through the list of input state abbreviations and plot them
        for state in self.main_states_list:
            if self.fortyeight:
                if self.final_usa.loc[self.final_usa['STUSPS'] == state]['WINNER'].values[0] == 'BLUE':
                    self.final_usa[self.final_usa.STUSPS == state].plot(ax=self.ax, color=self.rep_color, edgecolor='black', linewidth=self.line_thick).axis('off')
                elif self.final_usa.loc[self.final_usa['STUSPS'] == state]['WINNER'].values[0] == 'RED':
                    self.final_usa[self.final_usa.STUSPS == state].plot(ax=self.ax, color=self.dem_color, edgecolor='black', linewidth=self.line_thick).axis('off')
            else:
                if self.usa.loc[self.usa['STUSPS'] == state]['WINNER'].values[0] == 'BLUE':
                    self.usa[self.usa.STUSPS == state].plot(ax=self.ax, color=self.rep_color, edgecolor='b', linewidth=self.line_thick)
                elif self.usa.loc[self.usa['STUSPS'] == state]['WINNER'].values[0] == 'RED':
                    self.usa[self.usa.STUSPS == state].plot(ax=self.ax, color=self.dem_color, edgecolor='r', linewidth=self.line_thick)

        plt.show()