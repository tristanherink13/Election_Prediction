import argparse

from plot_state_results import PlotHistoricalData

class MainProgram():

    def __init__(self, year):
        self.year = int(year)
        plot_object = PlotHistoricalData(self.year)
        plot_object.merge_historical_data_into_gpd()
        plot_object.create_figure()

def main():
    parser = argparse.ArgumentParser(description='Input a year and return figure of presidential election data')
    parser.add_argument('--in', metavar='<inputyear>', required=False,
                       help='provide input year for plotting')

    args = parser.parse_args()
    input_year = getattr(args, 'in')

    # use input_year, otherwise default to latest election (2016)
    if input_year:
        MainProgram(input_year)
    else:
        MainProgram(2016)

if __name__ == '__main__':
    main()