import sys
import argparse

from state_map import StateMap
from calculations import Calculations
from prediction import Prediction

class MainProgram():

    def __init__(self, year):
        self.year = int(year)
        #plot_object = StateMap(self.year)
        #plot_object.merge_historical_data_into_gpd()
        #plot_object.create_legends()
        #plot_object.plot_legends()
        #plot_object.plot_states()
        prediction_object = Prediction()
        prediction_object.run_model()

def main():
    parser = argparse.ArgumentParser(description='Input a year and return figure of presidential election data')
    parser.add_argument('--in', metavar='<inputyear>', required=False,
                       help='provide input year for plotting')

    args = parser.parse_args()
    input_year = getattr(args, 'in')
    valid_years = ['1976', '1980', '1984', '1988', '1992', '1996',
                   '2000', '2004', '2008', '2012', '2016']

    # use input_year, otherwise default to latest election (2016)
    if not input_year:
        MainProgram(2016)
    elif input_year in valid_years:
        MainProgram(input_year)
    elif input_year not in valid_years:
        print('Please input a valid election year from 1976-2016')
        sys.exit()

if __name__ == '__main__':
    main()