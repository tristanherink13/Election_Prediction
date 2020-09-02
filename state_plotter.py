from historical_state_voting_calculations import HistoricalStateVotingCalculations

class StatePlotter():

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