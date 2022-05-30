"""
This script uses one of memory based collaborative filtering techniques which
is the Pearson correlation to calculate the similarity of people's taste when
it comes to movies and give recommendations based on received results
"""

import pandas as pd
from data_analysis import show_empty_cell_percentage
from data_analysis import show_hist_plot
from scipy.stats import pearsonr
import os

# Read Excel file containing data
df = pd.read_excel('./excel files/ratings_matrix_no_nulls.xlsx',
                   index_col="Movie Id", header=0)

# Transpose the DataFrame for convenience
df = df.transpose()

# Show handy information about the dataset
# show_empty_cell_percentage(df)
# show_hist_plot(df, bin_num=60)

# Reset the index to turn the values into a column
df = df.reset_index()

# Extract the DataFrame with my data
my_data = df[df['index'] == os.environ['LOGIN']]
my_data = my_data.melt().dropna()[1:]

# Erasing my data not to be messed up with friends data
df = df[:-1]

# List of movies I watched - basis for calculating the correlation
my_movielist = my_data['Movie Id'].values.tolist()

# Melt the DataFrame for convenience
friends_rates = df.melt(id_vars=['index']).dropna()

# Group by friends/ratings for further calculations
friends_grouped = friends_rates.groupby(['index'])
friends_rates_grouped = friends_rates.groupby(['Movie Id'])

# Sorting friends by amount of movies watched
friends_sorted = sorted(friends_grouped, key=lambda x: len(x[1]), reverse=True)

# Creating a dictionary for results
pearson_corr_dict = {}

# Sorting values and iterating over the dataset of movies that friends watched
my_rates = my_data.sort_values(by="Movie Id")
for friend, data in friends_sorted:
    data = data.sort_values(by="Movie Id")

    # Creating a DataFrame containing common movies
    my_common_movies = my_rates[my_rates['Movie Id'].isin(data['Movie Id']
                                                          .tolist())]

    # Creating a list of movies that me and my friend watched
    my_common_movies_list = my_common_movies['Movie Id'].tolist()

    friends_common_movies = data[data['Movie Id'].isin(my_common_movies_list)]

    friends_common_movies_list = my_common_movies['value'].tolist()

    common_movies_num = len(my_common_movies['value'].tolist())

    # Setting the minimum number of common movies for correlation to be precise
    # Minimum value for the function to work is 2
    min_common_movies = 5
    if common_movies_num > min_common_movies:
        corr = pearsonr(my_common_movies_list, friends_common_movies_list)[0]
    else:
        corr = 0

    pearson_corr_dict[friend] = corr

pearson_corr_df = pd.DataFrame.from_dict(pearson_corr_dict, orient='index')
pearson_corr_df.columns = ['correlation']
pearson_corr_df['friend'] = pearson_corr_df.index
pearson_corr_df.index = range(len(pearson_corr_df))

pearson_corr_df_sorted = pearson_corr_df.sort_values(by='correlation',
                                                     ascending=False)
