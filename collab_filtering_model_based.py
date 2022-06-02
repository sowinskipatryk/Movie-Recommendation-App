"""
This script uses the model based approach - one of collaborative filtering
techniques along with the memory based approach. The recommendations are
calculated based on items - movies, but this time we use a model to get the
results. This depends on building in this case two latency factors matrices
and use a technique called Matrix Factorization to calculate the values inside
of these matrices so that they can reproduce the original ratings matrix and
reduce memory used as we only need to store two small matrices instead of one of
huge size. Values are tuned by iterating and correcting the factors based on the
obtained error value calculated as the sum of the squares of the differences 
between the expected and obtained values
"""

import pandas as pd
import numpy as np
import os

# Set the number of latent features, steps, error tolerance (if this value is
# reached, the iteration stops), alpha and beta coefficients
latent_features_num = 3
steps_num = 1000
error_tolerance = 20000
alpha = 0.001
beta = 0.01

# Set username
username = os.environ['LOGIN']

# Read Excel file containing movie ratings
ratings = pd.read_excel('./excel_files/ratings_matrix.xlsx',
                        index_col="Movie Id", header=0)

# Transpose the DataFrame for convenience
ratings = ratings.transpose()

# Replace empty cells with zeros
ratings.fillna(0, inplace=True)

# Extract unseen movies
unseen_movies_mask = ratings.loc[username] == 0
unseen_movies_df = ratings.loc[username][unseen_movies_mask == True]
unseen_movies_list = unseen_movies_df.index.to_list()

# Extract the number of users and movies
users_num = ratings.shape[0]
movies_num = ratings.shape[1]

# Create matrices with random data as starting point of matrix factorization
user_factors = np.random.rand(users_num, latent_features_num)
movie_factors = np.random.rand(latent_features_num, movies_num)

# Extract users and movie ids to separate lists
users = ratings.index.values.tolist()
movie_ids = ratings.columns.values.tolist()

# Reset movie indexes and column names for easier iteration
ratings.reset_index(drop=True, inplace=True)
ratings.columns = range(ratings.columns.size)

""" For each step:
# a) iterate over each user and each movie to check if there is a rating for
# that particular movie and if there is - calculate the error as the difference
# between the rating given and the dot product of user and movie factors for
# specific user and specific movie and use this error to tune the model by
# changing user and movie factors
# b) calculate the error matrix as the dot product of latent features matrices
# c) calculate the error as the sum of squared differences between the actual
# ratings and the scores calculated using user and movie factors - if the error
# is small enough - stop the calculations
"""
for step in range(steps_num):
    for i in range(users_num):
        for j in range(movies_num):
            if ratings[j][i] > 0:
                eij = ratings[j][i] - np.dot(user_factors[i,:],
                                             movie_factors[:,j])

                for k in range(latent_features_num):
                    user_factors[i][k] = user_factors[i][k] + alpha * \
                                         (2 * eij * movie_factors[k][j] - beta
                                          * user_factors[i][k])
                    movie_factors[k][j] = movie_factors[k][j] + alpha * \
                                          (2 * eij * user_factors[i][k] - beta
                                           * movie_factors[k][j])

    error_matrix = np.dot(user_factors, movie_factors)
    error = 0

    for i in range(users_num):
        for j in range(movies_num):
            if ratings[j][i] > 0:
                error = error + pow(ratings[j][i] - np.dot(user_factors[i,:],
                                             movie_factors[:,j]), 2)

    if error < error_tolerance:
        break

    # Print process details
    print(f'Step: {step+1}')
    print(f'Error: {error}')

# Calculate the complete ratings matrix as the dot product of computed
# factors matrices
ratings_matrix_full = np.dot(user_factors, movie_factors)

# Round ratings to the nearest integer
ratings_matrix_full = ratings_matrix_full.round()

# Recreate the full movie ratings DataFrame
ratings_matrix_full_df = pd.DataFrame(ratings_matrix_full, index=users,
                                      columns=movie_ids)

# Print the filled movie ratings matrix
# print(ratings_matrix_full_df)

# Read Excel file containing data about movies
movies = pd.read_excel('./excel_files/movies.xlsx', header=0)

# Extract assumed ratings for specified user
user_assumptions = ratings_matrix_full_df.loc[username].reset_index()

# Merge movie ratings with movies information DataFrame
merged_movie_assumptions = user_assumptions.merge(movies, left_on='index',
                                                  right_on='Movie Id',
                                                  how='inner')

# Create a more intuitive name for ratings column
merged_movie_assumptions['Rating'] = merged_movie_assumptions[username]

# Set the movie id as index to filter by list of movie ids
merged_movie_assumptions.set_index('Movie Id', inplace=True)

# Filter the DataFrame by list of unwatched movies' ids
user_watchlist = merged_movie_assumptions.loc[unseen_movies_list]

# Sort the recommended movies by rating
user_watchlist_sorted = user_watchlist.sort_values(by='Rating',
                                                     ascending=False)

# Separate two main column from DataFrame to be shown
user_recommendations = user_watchlist_sorted[['Title', 'Rating']]

# Print user recommendations
print(user_recommendations.to_string())
