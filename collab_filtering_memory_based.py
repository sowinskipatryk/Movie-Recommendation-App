"""
This script uses one of memory based collaborative filtering techniques which
is the Pearson correlation to calculate the similarity of people's taste when
it comes to movies and give movie recommendations based on received results
"""

import pandas as pd
from data_analysis import show_empty_cell_percentage
from data_analysis import show_hist_plot
from scipy.stats import pearsonr
import os

# Read Excel file containing data
df = pd.read_excel('./excel_files/ratings_matrix.xlsx',
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

# Erase my data not to be messed up with friends data
df = df[:-1]

# Create a list of movies I watched - basis for calculating the correlation
my_movielist = my_data['Movie Id'].values.tolist()

# Melt the DataFrame for convenience
friends_rates = df.melt(id_vars=['index']).dropna()

# Group by friends/ratings for further calculations
friends_grouped = friends_rates.groupby(['index'])
friends_rates_grouped = friends_rates.groupby(['Movie Id'])

# Sort friends by amount of movies watched
friends_sorted = sorted(friends_grouped, key=lambda x: len(x[1]), reverse=True)

# Create a dictionary for results
pearson_corr_dict = {}

# Sort values and iterating over the dataset of movies that friends watched
my_rates = my_data.sort_values(by="Movie Id")
for friend, data in friends_sorted:
    data = data.sort_values(by="Movie Id")

    # Create a DataFrame containing my ratings of common movies
    my_common_movies = my_rates[my_rates['Movie Id'].isin(data['Movie Id']
                                                          .tolist())]

    # Create a list of movies that me and my friend watched
    my_common_movies_list = my_common_movies['Movie Id'].tolist()

    # Create a DataFrame containing friend's ratings of common movies
    friends_common_movies = data[data['Movie Id'].isin(my_common_movies_list)]

    # Create a list of rates that my friend gave
    friends_common_movies_list = my_common_movies['value'].tolist()

    # Number of common movies
    common_movies_num = len(my_common_movies['value'].tolist())

    # Set the minimum number of common movies for correlation to be precise
    # Minimum value for the function to work is 2
    min_common_movies = 5
    if common_movies_num > min_common_movies:
        corr = pearsonr(my_common_movies_list, friends_common_movies_list)[0]
    else:
        corr = 0

    # Add results to a dictionary
    pearson_corr_dict[friend] = corr

# Create a DataFrame for correlation data
pearson_corr_df = pd.DataFrame.from_dict(pearson_corr_dict, orient='index')
pearson_corr_df.columns = ['correlation']
pearson_corr_df['friend'] = pearson_corr_df.index
pearson_corr_df.index = range(len(pearson_corr_df))

# Sort values from highest to lowest correlation
pearson_corr_df_sorted = pearson_corr_df.sort_values(by='correlation',
                                                     ascending=False)

# Merge DataFrames
merged_corr_df = pearson_corr_df_sorted.merge(friends_rates, left_on='friend',
                                  right_on='index', how='inner')

# Set the minimum number of rates needed for movie to be recommended
# To avoid recommendations based on one friend with high similarity
min_friends_rates = 3

# Create a mask DataFrame with movies at least n friends watched
min_sum_df = (merged_corr_df.groupby('Movie Id').count()['value'] >=
              min_friends_rates).reset_index()

# Create a list with movies at least n friends watched
min_sum_df_list = min_sum_df[min_sum_df['value'] == True]['Movie Id'].tolist()

# Overwrite the DataFrame with recommended movies with only the titles that
# meet the criteria mentioned above
merged_corr_df = merged_corr_df[merged_corr_df['Movie Id'].isin(min_sum_df_list)]

# Calculate Weighted Rating
merged_corr_df['weighted_rating'] = merged_corr_df['correlation'] * \
                                    merged_corr_df['value']

calc_df = merged_corr_df.groupby('Movie Id').sum()[['correlation',
                                                    'weighted_rating']]

calc_df.columns = ['correlation_sum', 'weighted_rating_sum']

# Create recommendations DataFrame with calculated WARR - weighted average
# recommendation rating
recommendations = pd.DataFrame()
recommendations['WARR'] = calc_df['weighted_rating_sum'] / \
                          calc_df['correlation_sum']
recommendations['Movie Id'] = calc_df.index
recommendations = recommendations.sort_values(by='WARR', ascending=False)

# Create a list for sorting purposes
recommendation_list = recommendations['Movie Id'].tolist()

# Load Excel file with movies data
movies = pd.read_excel('./excel_files/movies.xlsx', index_col='Movie Id',
                       header=0)

movies = movies.drop(columns=movies.columns[0])

# Erase movies I watched
movies_unseen = [movie for movie in recommendation_list if movie not in
                 my_movielist]

# Filter and show movie recommendations
movie_recommendations = movies.loc[movies_unseen]
print(movie_recommendations)
