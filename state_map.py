import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from state_plotter import StatePlotter

class StateMap(StatePlotter):

    def merge_historical_data_into_gpd(self):
        # append winner and electoral votes data to geopandas df
        self.usa['WINNER'] = self.winner_ordered_list
        self.usa['VOTES'] = self.electoral_votes_ordered_list

    def create_legends(self):
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
        self.legend_list = []
        self.percent_legend_list = []
        alpha_ordered_states = self.calculations.alpha_ordered_states
        alpha_ordered_colors = self.calculations.alpha_ordered_colors
        alpha_ordered_electoral_votes = self.calculations.alpha_ordered_electoral_votes
        alpha_ordered_percents = self.calculations.alpha_ordered_percents

        # label each state red/blue and count up electoral votes
        for i, state in enumerate(alpha_ordered_states):
            if alpha_ordered_colors[i] == 'BLUE':
                self.legend = mpatches.Patch(color=self.dem_color,
                              label='{} : {}'.format(state,
                              alpha_ordered_electoral_votes[i]))
            else:
                self.legend = mpatches.Patch(color=self.rep_color,
                              label='{} : {}'.format(state,
                              alpha_ordered_electoral_votes[i]))
            self.legend_list.append(self.legend)
        
        # variables for first legend
        total_dem_electoral_votes = self.calculations.total_dem_electoral_votes
        total_rep_electoral_votes = self.calculations.total_rep_electoral_votes
        dem_candidate = self.calculations.dem_candidate
        rep_candidate = self.calculations.rep_candidate
        dem_pop_vote = self.calculations.dem_pop_vote
        rep_pop_vote = self.calculations.rep_pop_vote

        # add label for running candidates and popular votes
        if total_dem_electoral_votes > total_rep_electoral_votes:
            self.win_legend = mpatches.Patch(color=self.dem_color, label=dem_candidate)
        else:
            self.win_legend = mpatches.Patch(color=self.rep_color, label=rep_candidate)

        if dem_pop_vote > rep_pop_vote:
            self.popular_win_legend = mpatches.Patch(color=self.dem_color,
                                      label='{} : {}'.format(dem_candidate, dem_pop_vote))
            self.popular_lose_legend = mpatches.Patch(color=self.rep_color,
                                       label='{} : {}'.format(rep_candidate, rep_pop_vote))
        else:
            self.popular_win_legend = mpatches.Patch(color=self.rep_color,
                                      label='{} : {}'.format(rep_candidate, rep_pop_vote))
            self.popular_lose_legend = mpatches.Patch(color=self.dem_color,
                                       label='{} : {}'.format(dem_candidate, dem_pop_vote))

        # variables for Voting Statistics legend
        dem_states_won = self.calculations.dem_states_won
        rep_states_won = self.calculations.rep_states_won
        dem_state_percentage = self.calculations.dem_state_percentage
        rep_state_percentage = self.calculations.rep_state_percentage

        # create legend for electoral vote breakdown
        self.dem_legend = mpatches.Patch(color=self.dem_color,
                          label='{} votes ({}%)'.format(total_dem_electoral_votes, dem_state_percentage))
        self.dem_state_legend = mpatches.Patch(color=self.dem_color,
                                label='{} states won'.format(dem_states_won))
        self.rep_legend = mpatches.Patch(color=self.rep_color,
                          label='{} votes ({}%)'.format(total_rep_electoral_votes, rep_state_percentage))
        self.rep_state_legend = mpatches.Patch(color=self.rep_color,
                                label='{} states won'.format(rep_states_won))

        # create legend for voting statistics by state
        if dem_state_percentage > rep_state_percentage:
            self.third_legend = [self.dem_legend, self.dem_state_legend, self.rep_legend, self.rep_state_legend]
        else:
            self.third_legend = [self.rep_legend, self.rep_state_legend, self.dem_legend, self.dem_state_legend]

        # create legend for close, or "swing", states
        for i, state in enumerate(alpha_ordered_states):
            if self.year != 2020:
                if alpha_ordered_percents[i] < 2 and alpha_ordered_colors[i] == 'BLUE':
                    percent_legend = mpatches.Patch(color=self.dem_color,
                                                    label='{} : {}%'.format(state,
                                                    alpha_ordered_percents[i]))
                    self.percent_legend_list.append(percent_legend)
                elif alpha_ordered_percents[i] < 2 and alpha_ordered_colors[i] == 'RED':
                    percent_legend = mpatches.Patch(color=self.rep_color,
                                                    label='{} : {}%'.format(state,
                                                    alpha_ordered_percents[i]))
                    self.percent_legend_list.append(percent_legend)
            else:
                if (2.2 <= alpha_ordered_percents[i] <= 3.5 or alpha_ordered_percents[i] < .1 
                and alpha_ordered_colors[i] == 'BLUE'):
                    percent_legend = mpatches.Patch(color=self.dem_color,
                                                    label='{} : {}%'.format(state,
                                                    alpha_ordered_percents[i]))
                    self.percent_legend_list.append(percent_legend)
                elif (2.2 <= alpha_ordered_percents[i] <+ 3.5 or alpha_ordered_percents[i] < .1 
                and alpha_ordered_colors[i] == 'RED'):
                    percent_legend = mpatches.Patch(color=self.rep_color,
                                                    label='{} : {}%'.format(state,
                                                    alpha_ordered_percents[i]))
                    self.percent_legend_list.append(percent_legend)

    def plot_legends(self):
        # plot legends
        x_align = .96
        winner_legend = plt.legend(
                                handles=[self.win_legend], title='Winner', bbox_to_anchor=(x_align, 1.01),
                                loc='upper left', fontsize='small', shadow=True
                                )

        candidate_legend = plt.legend(
                                handles=[self.popular_win_legend, self.popular_lose_legend], 
                                title='Candidate : Popular Vote', bbox_to_anchor=(x_align, .925),
                                loc='upper left', fontsize='small', shadow=True
                                )

        electoral_legend = plt.legend(
                                handles=self.legend_list, title='Electoral Votes', bbox_to_anchor=(x_align, .815),
                                loc='upper left', fontsize='small', shadow=True, ncol=3
                                )

        vote_legend = plt.legend(
                                handles=self.third_legend, title='Voting Statistics', bbox_to_anchor=(x_align, .3),
                                loc='upper left', fontsize=8, shadow=True, ncol=2
                                )
        
        percent_legend = plt.legend(
                                handles=self.percent_legend_list, title='Swing States', bbox_to_anchor=(x_align, .19),
                                loc='upper left', fontsize=7.45, shadow=True, ncol=3
                                )
        
        # Add overwritten legends manually
        self.ax.add_artist(winner_legend)
        self.ax.add_artist(candidate_legend)
        self.ax.add_artist(electoral_legend)
        self.ax.add_artist(vote_legend)
        self.ax.add_artist(percent_legend)

    def plot_states(self):
        # remove Alaska and Hawaii from map for aesthetics 
        unique_abbrevs = self.calculations.unique_abbrevs
        [self.main_states_list.append(st) for st in unique_abbrevs if st != 'AK' and st != 'HI']
        final_usa = self.usa[(self.usa.STUSPS != 'AK') & (self.usa.STUSPS != 'HI')]

        # go through the list of state abbreviations and plot them
        for state in self.main_states_list:
            if final_usa.loc[final_usa['STUSPS'] == state]['WINNER'].values[0] == 'BLUE':
                final_usa[final_usa.STUSPS == state].plot(ax=self.ax, color=self.dem_color,
                                              edgecolor='black', linewidth=self.line_thick).axis('off')
            elif final_usa.loc[final_usa['STUSPS'] == state]['WINNER'].values[0] == 'RED':
                final_usa[final_usa.STUSPS == state].plot(ax=self.ax, color=self.rep_color,
                                              edgecolor='black', linewidth=self.line_thick).axis('off')
        plt.show()