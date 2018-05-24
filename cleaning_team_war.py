import pandas as pd
import sys

# Read in the csv file as a dataframe. Accepts the string which is the path to the data file.
def read_season_as_dataframe(br_data):
    season = pd.read_csv(br_data)
    return season

# Drop the unused rank column
def drop_rank(df):
    df = df.drop('Rk', axis = 1)
    return df

# Drop the unused final row
def drop_final_row(df):
    df = df.drop(df.index[len(df)-1])
    return df

# Sort each column
def sort_columns(df):
    columns = list(df.columns)
    for column in columns:
        column_list = list(df[column])
        sorted_column_list = sorted(column_list)

        for i in range(0,len(df)):
            df[column][i] = sorted_column_list[i]
    return df



data = sys.argv[1]
season_df = read_season_as_dataframe(data)
season_df = drop_rank(season_df)
season_df = drop_final_row(season_df)
season_df = sort_columns(season_df)
print(season_df.head())

