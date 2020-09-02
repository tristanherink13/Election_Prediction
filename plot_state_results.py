import pandas as pd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib

from election_data import ElectionData
from historical_state_voting_calculations import HistoricalStateVotingCalculations

class StatePlotter:

    def __init__(self, year):
        # initialize attributes
        self.year = year
        self.main_states_list = []
        # get StateVotingCalculations attributes
        self.calculations = HistoricalStateVotingCalculations()
        self.winner_method = self.calculations.determine_historical_winner(self.year)
        # set attributes
        self.winner_ordered_list = self.calculations.winner_ordered_list
        self.state_ordered_list = self.calculations.state_ordered_list
        self.electoral_votes_ordered_list = self.calculations.electoral_votes_ordered_list
        self.usa = self.calculations.usa

        print('plotting data...')

class PlotHistoricalData(StatePlotter):

    def merge_historical_data_into_gpd(self):
        # append winner and electoral votes data to geopandas df
        self.usa['WINNER'] = self.winner_ordered_list
        self.usa['VOTES'] = self.electoral_votes_ordered_list
    
    def create_figure(self):
        # initialize variables
        fortyeight = True
        xmin = -200
        xmax = -65
        ymin = 15
        ymax = 75
        # instantiate a matplotlib figure
        fig, ax = plt.subplots(figsize=(20,8))
        # shift states plot over to left
        ax = fig.add_axes([0.02, 0.02, 0.8, 0.8])
        # remove axis around map
        fig.subplots_adjust(wspace=0, top=1, right=1, left=0, bottom=0)
        # set title
        ax.set_title('Presidential Winner By State, {}'.format(self.year), fontsize=14, x=.625)
        # choose color scheme and line thickness for dem/rep
        dem_color = '#3A34DB'
        rep_color = '#DC2C2C'
        line_thick = 1

        # start creating labels for legends
        handles, labels = ax.get_legend_handles_labels()
        legend_list = []
        alpha_ordered_states = self.calculations.alpha_ordered_states
        alpha_ordered_colors = self.calculations.alpha_ordered_colors
        alpha_ordered_electoral_votes = self.calculations.alpha_ordered_electoral_votes

        # label each state red/blue and count up electoral votes
        for i, state in enumerate(alpha_ordered_states):
            if alpha_ordered_colors[i] == 'BLUE':
                legend = mpatches.Patch(color=dem_color, label='{} : {}'.format(state, alpha_ordered_electoral_votes[i]))
            else:
                legend = mpatches.Patch(color=rep_color, label='{} : {}'.format(state, alpha_ordered_electoral_votes[i]))
            legend_list.append(legend)
        
        # variables for first legend
        total_dem_electoral_votes = self.calculations.total_dem_electoral_votes
        total_rep_electoral_votes = self.calculations.total_rep_electoral_votes
        dem_candidate = self.calculations.dem_candidate
        rep_candidate = self.calculations.rep_candidate
        dem_pop_vote = self.calculations.dem_pop_vote
        rep_pop_vote = self.calculations.rep_pop_vote

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

        # variables for Voting Statistics legend
        dem_states_won = self.calculations.dem_states_won
        rep_states_won = self.calculations.rep_states_won
        dem_state_percentage = self.calculations.dem_state_percentage
        rep_state_percentage = self.calculations.rep_state_percentage

        # create legend for electoral vote breakdown
        dem_legend = mpatches.Patch(color=dem_color, label='{} votes ({}%)'.format(total_dem_electoral_votes, dem_state_percentage))
        dem_state_legend = mpatches.Patch(color=dem_color, label='{} states won'.format(dem_states_won))
        rep_legend = mpatches.Patch(color=rep_color, label='{} votes ({}%)'.format(total_rep_electoral_votes, rep_state_percentage))
        rep_state_legend = mpatches.Patch(color=rep_color, label='{} states won'.format(rep_states_won))

        # create legend for voting statistics by state
        if dem_state_percentage > rep_state_percentage:
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

        unique_abbrevs = self.calculations.unique_abbrevs
        [self.main_states_list.append(st) for st in unique_abbrevs if st != 'AK' and st != 'HI']

        if 'AK' and 'HI' in self.main_states_list:
            fortyeight = False
            ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        elif 'AK' in self.main_states_list:
            final_usa = self.usa[self.usa.STUSPS != 'HI']
            ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        elif 'HI' in self.main_states_list:
            final_usa = self.usa[self.usa.STUSPS != 'AK']
        else:
            final_usa = self.usa[(self.usa.STUSPS != 'AK') & (self.usa.STUSPS != 'HI')]

        # go through the list of input state abbreviations and plot them
        for state in self.main_states_list:
            if fortyeight:
                if final_usa.loc[final_usa['STUSPS'] == state]['WINNER'].values[0] == 'BLUE':
                    final_usa[final_usa.STUSPS == state].plot(ax=ax, color=dem_color, edgecolor='black', linewidth=line_thick).axis('off')
                elif final_usa.loc[final_usa['STUSPS'] == state]['WINNER'].values[0] == 'RED':
                    final_usa[final_usa.STUSPS == state].plot(ax=ax, color=rep_color, edgecolor='black', linewidth=line_thick).axis('off')
            else:
                if self.usa.loc[self.usa['STUSPS'] == state]['WINNER'].values[0] == 'BLUE':
                    self.usa[self.usa.STUSPS == state].plot(ax=ax, color=dem_color, edgecolor='black', linewidth=line_thick).axis('off')
                elif self.usa.loc[self.usa['STUSPS'] == state]['WINNER'].values[0] == 'RED':
                    self.usa[self.usa.STUSPS == state].plot(ax=ax, color=rep_color, edgecolor='black', linewidth=line_thick).axis('off')

        plt.show()