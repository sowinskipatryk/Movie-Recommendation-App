"""
This script uses one of memory based collaborative filtering techniques which
is the Pearson correlation to calculate the similarity of people's taste when
it comes to movies and give movie recommendations based on received results

In this version, empty cells with unrated movies are not skipped but given
values equal to zero - this approach is supposed to result in increased
efficiency of the method used
"""

import pandas as pd
from helper_functions.data_analysis import show_empty_cell_percentage
from helper_functions.data_analysis import show_hist_plot
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

# Replace empty cells with zeros
df.fillna(0, inplace=True)

# Extract the DataFrame with my ratings
my_data = df[df['index'] == os.environ['LOGIN']
my_data = my_data.melt()[1:]

# Erase the data with my ratings from df not to be messed up with friends data
df = df[:-1]

# Melt the DataFrame for convenience
friends_rates = df.melt(id_vars=['index'])

# Group by friends for further calculations
friends_grouped = friends_rates.groupby(['index'])

# Create a list of tuples containing friends names and number of movies watched
friends_rates_num = [(sum(y['value'] != 0), x) for x, y in friends_grouped]

# Sort the list of tuples by amount of movies watched
friends_sorted = sorted(friends_rates_num, reverse=True)

# Extract a list of friends with most movies watched
friends_sorted_list = [friends_sorted[i][1] for i in range(len(friends_sorted))]

# Sort the data by the number of movies watched
sorted_data = sorted(friends_grouped, key=lambda x: friends_sorted_list.index(x[0]))

# Create a dictionary for correlation scores
pearson_corr_dict = {}

# Filter out ratings and convert them to a list
my_rates = my_data['value']
my_rates_list = my_rates.tolist()

for friend, data in sorted_data:

    # Create a list of friend's rates
    friends_rates_list = data['value'].tolist()

    # Calculate the Pearson Correlation score
    corr = pearsonr(my_rates_list, friends_rates_list)[0]

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

# Replace empty cells with zeros
pearson_corr_df_sorted.fillna(0, inplace=True)

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

movies_unseen_df = my_data[my_data['value'] == 0]
movies_unseen_list = movies_unseen_df['Movie Id'].tolist()

# Erase movies I watched
movies_unseen = [movie for movie in recommendation_list if movie in
                 movies_unseen_list]

# Filter and show movie recommendations
movie_recommendations = movies.loc[movies_unseen]
print(movie_recommendations)
