"""
This script uses the content filtering technique based on items features - in 
this case movie genres - to calculate first the user's movie taste (favorite 
movie genres) based on the ratings given by said user to already watched movies 
and then utilizes the result values to compare them with yet unwatched movies to
create a recommendation list of movies for said user
"""

import pandas as pd
import os

# Read Excel file containing data about movies
movies_df = pd.read_excel('./excel_files/movies.xlsx', index_col='Movie Id',
                          header=0)

# Split the genres for each movie to be stored in a list
movies_df['Genre'] = movies_df['Genre'].str.split(' / ')
movies_df.reset_index(inplace=True)

# Copy the DataFrame and make a matrix of zeros and ones to store information
# about the genres for each movie
movie_genres_df = movies_df.copy()
for index, row in movies_df.iterrows():
    for genre in row['Genre']:
        movie_genres_df.at[index, genre] = 1

# Replace empty cells with zeros and reset indexes
movie_genres_df.fillna(0, inplace=True)
movie_genres_df.reset_index(inplace=True)

# Read Excel file containing data about movie ratings
friends_rates_df = pd.read_excel('./excel_files/ratings_matrix.xlsx',
                                 index_col="Movie Id", header=0)

# Transpose the DataFrame and reset indexes
friends_rates_df = friends_rates_df.transpose()
friends_rates_df = friends_rates_df.reset_index()

# Extract my ratings from the DataFrame, restructure the DataFrame and
# replace empty cells with zeros
my_rates_df = friends_rates_df[friends_rates_df['index'] == os.environ['LOGIN']]
my_rates_df = my_rates_df.melt()[1:]
my_rates_df.fillna(0, inplace=True)

# Once again replace empty cells with zeros this time for friends ratings
# Erase the last row which contains my data and restructure the DataFrame
friends_rates_df.fillna(0, inplace=True)
friends_rates_df = friends_rates_df[:-1]
friends_rates_df = friends_rates_df.melt(id_vars=['index'])

# Drop columns with movie information to leave only the movie genre information
movie_genres_df = movie_genres_df.drop(movie_genres_df.columns[0:8], axis=1)

# Drop the unnecessary column
movies_df = movies_df.drop(movies_df.columns[1], axis=1)

# Reset indexes
my_rates_df.reset_index(inplace=True, drop=True)

# Calculate the dot product of movie genre values and my ratings
my_fav_genres_df = movie_genres_df.transpose().dot(my_rates_df['value'])

# Print my favourite movie genres as calculated above
print(my_fav_genres_df.reset_index().sort_values([0], ascending=False))

# Calculate the scores obtained by each movie based on my favorite movie genres
recommendations = ((movie_genres_df * my_fav_genres_df).sum(axis=1)) / \
                  (my_fav_genres_df.sum())

# Sort the recommendations
recommendations = recommendations.sort_values(ascending=False)

# Filter the unseen movies
movies_unseen = my_rates_df[my_rates_df['value'] == 0]

# Convert the unseen movies DataFrame's indexes to a list
movies_unseen_list = movies_unseen.index.tolist()

# Convert the recommendations DataFrame's indexes to a list
recommendations_list = recommendations.index.tolist()

# Filter the recommendation list on unseen movies
recommendations_unseen_list = [movie for movie in recommendations_list if movie
                               in movies_unseen_list]

# Reset the indexes for movies DataFrame
movies_df = movies_df.reset_index()

# Sort the movies DataFrame on unwatched movies list
recommendations_unseen = movies_df.loc[recommendations_unseen_list]

# Print the recommended movies titles
print(recommendations_unseen['Title'])
