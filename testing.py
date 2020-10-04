import sys
import os
import ast
import pandas as pd

# import prediction results and convert to df
file_path = os.path.join(sys.path[0], 'Datasets', 'model_outcomes', 'predictions_97_rf_midterms.csv')

df = pd.read_csv(file_path)

winner_series = df.groupby(['Code', 'Winner'])['Population'].sum()

print(df['Population'])

df_2 = winner_series.to_frame().reset_index()
df_2.sort_values('Population', inplace=True)
df_2.drop_duplicates(subset='Code', keep='last',inplace=True)
df_2.sort_values('Code', inplace=True)

df_2 = df_2.replace(1.0, 'RED')
df_2 = df_2.replace(0.0, 'BLUE')

file_path_2 = os.path.join(sys.path[0], 'Datasets', 'electoral_votes_per_state.txt')
file_path_3 = os.path.join(sys.path[0], 'Datasets', 'state_acronym.csv')

with open(file_path_2, 'r') as data:
    electoral_votes_per_state_per_year_dict = ast.literal_eval(data.read())

df_3 = pd.read_csv(file_path_3)

biden_counter = 0
trump_counter = 0
predicted_blue_states = []
predicted_red_states = []
for i, row in enumerate(df_2.values):
    if row[1].strip() == 'BLUE':
        predicted_blue_states.append(df_3['State'][i])
        biden_counter += electoral_votes_per_state_per_year_dict[2016][i]
    elif row[1].strip() == 'RED':
        predicted_red_states.append(df_3['State'][i])
        trump_counter += electoral_votes_per_state_per_year_dict[2016][i]

if biden_counter > trump_counter:
    print('BIDEN WINS: {} to {}'.format(biden_counter, trump_counter))
elif trump_counter > biden_counter:
    print('TRUMP WINS: {} to {}'.format(trump_counter, biden_counter))

blue_state_polls_dict = {'Arizona':62, 'California':99, 'Colorado':88, 'Connecticut':99,
                    'Delaware':99, 'District of Columbia':99, 'Florida':58, 'Hawaii':99,
                    'Illinois':99, 'Maine':88, 'Maryland':99, 'Massachusetts':99,
                    'Michigan':86, 'Minnesota':88, 'Nevada':82, 'New Hampshire':77,
                    'New Jersey':98, 'New Mexico':95, 'New York':99, 'North Carolina':53,
                    'Ohio':52, 'Oregon':93, 'Pennsylvania':79, 'Rhode Island':99,
                    'Vermont':99, 'Virginia':96, 'Washington':99, 'Wisconsin':81}
red_state_polls_dict = {'Alabama':97, 'Alaska':79, 'Arkansas':94, 'Georgia':59, 'Idaho':99,
                   'Indiana':97, 'Iowa':63, 'Kansas':94, 'Kentucky':99, 'Louisiana':91,
                   'Mississippi':87, 'Missouri':91, 'Montana':87, 'Nebraska':99,
                   'North Dakota':99, 'Oklahoma':99, 'South Carolina':89, 'South Dakota':97,
                   'Tennessee':96, 'Texas':72, 'Utah':97, 'West Virginia':99, 'Wyoming':99}

blue_state_polls = list(blue_state_polls_dict.keys())
blue_state_percentages = list(blue_state_polls_dict.values())
red_state_polls = list(red_state_polls_dict.keys())
red_state_percentages = list(red_state_polls_dict.values())
blue_for_sure = []
probably_blue = []
red_for_sure = []
probably_red = []
battleground_list = []
agree_list = []
disagree_list = []
middle_ground_blue_list = []
middle_ground_red_list = []

for i, state in enumerate(blue_state_polls):
    if blue_state_percentages[i] > 85:
        blue_for_sure.append(state)
    elif blue_state_percentages[i] > 65:
        probably_blue.append(state)
    else:
        battleground_list.append(state)

for j, state in enumerate(red_state_polls):
    if red_state_percentages[j] > 85:
        red_for_sure.append(state)
    elif red_state_percentages[j] > 65:
        probably_red.append(state)
    else:
        battleground_list.append(state)

for state in predicted_blue_states:
    if state in blue_for_sure or state in probably_blue:
        agree_list.append(state)
    elif state in battleground_list:
        if state in blue_state_polls:
            middle_ground_blue_list.append([state, 'BLUE: {}'.format(blue_state_polls_dict[state])])
        elif state in red_state_polls:
            middle_ground_blue_list.append([state, 'RED: {}'.format(red_state_polls_dict[state])])
    else:
        if state in blue_state_polls:
            disagree_list.append([state, blue_state_polls_dict[state]])
        elif state in red_state_polls:
            disagree_list.append([state, red_state_polls_dict[state]])
        
for state in predicted_red_states:
    if state in red_for_sure or state in probably_red:
        agree_list.append(state)
    elif state in battleground_list:
        if state in blue_state_polls:
            middle_ground_red_list.append([state, 'BLUE: {}'.format(blue_state_polls_dict[state])])
        elif state in red_state_polls:
            middle_ground_red_list.append([state, 'RED: {}'.format(red_state_polls_dict[state])])
    else:
        if state in blue_state_polls:
            disagree_list.append([state, blue_state_polls_dict[state]])
        elif state in red_state_polls:
            disagree_list.append([state, red_state_polls_dict[state]])

print('DISAGREE ON: {}'.format(disagree_list))
#print('AGREE ON: {}'.format(agree_list))
print('MIDDLE GROUND BLUE: {}'.format(middle_ground_blue_list))
print('MIDDLE GROUND RED: {}'.format(middle_ground_red_list))
print('BLUE STATES: {}'.format(predicted_blue_states))
print('RED STATES: {}'.format(predicted_red_states))

df_2.to_csv('winning.csv')