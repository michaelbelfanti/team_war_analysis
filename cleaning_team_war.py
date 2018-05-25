import pandas as pd
import sys

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

# Add a 'Year' column
def add_year(df):
    df_with_year = df.copy()
    year = [data[10:14]]
    year_list = len(df)*year
    df_with_year.insert(loc = 1, column = 'Year', value = year_list) 
    return df_with_year

def remove_teams_from_entries(df):
    df_with_no_teams = df.copy()
    numeric_columns = list(df.columns)[2:]
    for column in numeric_columns:
        for i in range(0,len(df)):
            df_with_no_teams[column][i] = float(df[column][i][3:])
    return df_with_no_teams

data = sys.argv[1]
season_df = read_season_as_dataframe(data)
season_df = drop_rank(season_df)
season_df = drop_final_row(season_df)
season_df = sort_columns(season_df)
season_df = add_team(season_df)
season_df = add_year(season_df)
season_df = remove_teams_from_entries(season_df)
print(season_df.head())





