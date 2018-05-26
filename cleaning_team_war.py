import pandas as pd
import sys
import os

# Read in the csv file as a dataframe. Accepts the string which is the path to the data file.
def read_season_as_dataframe(br_data):
    season = pd.read_csv(br_data)
    return season

# Drop the unused rank column
def drop_rank(df):
    df_drop_rank = df.drop('Rk', axis = 1)
    return df_drop_rank

# Drop the unused final row
def drop_final_row(df):
    df_drop_final_row = df.drop(df.index[len(df)-1])
    return df_drop_final_row

# Sort each column
def sort_columns(df):
    columns = list(df.columns)
    df_sorted = df.copy()
    for column in columns:
        column_list = list(df[column])
        sorted_column_list = sorted(column_list)

        for i in range(0,len(df)):
            df_sorted[column][i] = sorted_column_list[i]
    return df_sorted

# Add a 'Team' column
def add_team(df):
    df_with_teams = df.copy()
    teams_list = []
    for i in range(0,len(df)):
        teams_list += [df['Total'][i][0:3]]
    df_with_teams.insert(loc = 0, column = 'Team', value = teams_list)
    return df_with_teams


# Extract digits
def extract_digits(str):
    digits = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']
    str_digits =''
    for character in str:
        if character in digits:
            str_digits += character
    str_digits = str_digits.strip('.')
    return str_digits

# Add year
def add_year(df1, str):
    year = extract_digits(str)
    year_list = len(df1)*[year]
    df1.insert(loc = 1, column = 'Year', value = year_list)
    return df1

# Clean the individual entries
def remove_teams_from_entries(df):
    numeric_columns = list(df.columns)[1:]
    for column in numeric_columns:
        for i in range(0,len(df)):
            df[column][i] = float(extract_digits(df[column][i]))
    return df

# Add a column for actual wins
def add_wins(war_df, standings_df):
    team_wins = []
    for i in range(0,len(standings_df)-1):
        team = standings_df['Tm'][i]
        league = standings_df['Lg'][i]
        wins = float(standings_df['W'][i])
        if league == 'NL':
            team_wins += [(team,wins)]
    team_wins = sorted(team_wins)

    sorted_wins = []
    for i in range(0,len(team_wins)):
        wins =team_wins[i][1]
        sorted_wins += [wins]

    war_df.insert(loc = 2, column = 'Wins', value = sorted_wins)

    return war_df

# Rename some columns

def rename_columns(df):
    columns = list(df.columns)
    columns[3] = 'TeamWAR'
    columns[4] = 'AllP'
    df.columns = columns
    return df 

"""
data = sys.argv[1]
wins_data = sys.argv[2]
wins_df = pd.read_csv(wins_data)
season_df = read_season_as_dataframe(data)
season_df = drop_rank(season_df)
season_df = drop_final_row(season_df)
season_df = sort_columns(season_df)
season_df = add_team(season_df)
season_df = add_year(season_df, wins_data)
season_df = remove_teams_from_entries(season_df)
season_df = add_wins(season_df,wins_df)
season_df = rename_columns(season_df)
print(season_df.head())
"""
# Process data for one season
def process_season(br_war_data, br_standings_data):
    war_df = pd.read_csv(br_war_data)
    standings_df = pd.read_csv(br_standings_data)
    war_df = drop_rank(war_df)
    war_df = drop_final_row(war_df)
    war_df = sort_columns(war_df)
    war_df = add_team(war_df)
    war_df = add_year(war_df,br_standings_data)
    war_df = remove_teams_from_entries(war_df)
    war_df = add_wins(war_df,standings_df)
    war_df = rename_columns(war_df)
    
    return war_df

# Process and combine multiple seasons in a file
def combine_seasons(war_data_directory, standings_data_directory):
    war_data_list = os.listdir(war_data_directory)
    standings_data_list = os.listdir(standings_data_directory)
    season_dfs = []
    for i in range(0,len(war_data_list)):
        war_file = os.path.join(war_data_directory, war_data_list[i])
        standings_file = os.path.join(standings_data_directory, standings_data_list[i])
        season_df = process_season(war_file, standings_file)
        season_dfs += [season_df]
    return pd.concat(season_dfs, ignore_index = True)






