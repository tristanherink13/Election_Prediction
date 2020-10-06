from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

final_df = pd.DataFrame()

years = [2014]

# iterate over midterm election years
for year in years:
    # page to be scraped
    url_page = 'https://ballotpedia.org/Election_results,_{}'.format(year)

    # send request and pull relevant table data
    response = requests.get(url_page)
    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all(class_='collapsible')
    tables = tables[:-1]

    # initialize individual year dict and special states
    year_dict = {}

    # iterate over all items in tables
    for i, item in enumerate(tables):
        votes_per_party = tables[i].findChildren('td', {'width': '100'})
        votes_per_party = votes_per_party[:-1]
        parties = tables[i].findChildren('td', {'width': '75px'})
        parties = parties[1:]
        states = tables[i].findChildren('th')
        temp_dict = {}
        sum_others = 0

        # iterate over individual parties
        for j, party in enumerate(parties):
            if 'Republican' in party.text:
                temp_dict.update({party.text.strip() : int(votes_per_party[j].text.replace(',',''))})
            elif 'Democrat' in party.text:
                temp_dict.update({party.text.strip() : int(votes_per_party[j].text.replace(',',''))})
            else:
                sum_others += int(votes_per_party[j].text.replace(',',''))
        # add sum of all other parties together into dict
        temp_dict.update({'Other' : sum_others})

        # add states as key to dict {state : {party : votes}}
        for state in states:
            state = state.text.split(', ')[1]
            if 'General' in state:
                state = state.split(' General Election')[0]
            if 'Primary' in state:
                state = state.split(' Primary Election')[0]
            year_dict.update({state : temp_dict})

    # convert dict to df and append to overall dict
    year_df = pd.DataFrame(year_dict)
    year_df['Year'] = year
    final_df = pd.concat([final_df, year_df], axis=0)

# write outputs to csv
final_df.to_csv('2014_midterm_data.csv')