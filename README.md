# Movie-Recommendation-App

The purpose of this program is to present some techniques of movie recommendation systems used, among others, by streaming services.
<br/><br/>

<h3>/ Collaborative Filtering - Memory Based - Pearson Correlation /</h3>

In the first version of the program, a collaborative filtering technique is implemented using similarities between users to find people that rate movies alike and thus movies watched by one person will probably be rated high by another person if the correlation score between these two users is high. The similarity between users (friends) was calculated using Pearson Correlation score which is one of the memory based methods. 

<br/>
<h3>/ Content Filtering - Item Based - Dot product of two matrices /</h3>

In the second version of the program, a content filtering technique is used which means that the movie recommendation list is calculated based on the correlation between items features - in this case the movie genres. To calculate the correlation first it is necessary to calculate the user's movie taste (a data structure containing favorite movie genres) based on the ratings given by said user to already watched movies that have some features to be identified (e.g. movie genre).
Then the result values are used to compare them with yet unwatched movies and so the movies that have the highest score (have the most features appreciated by the user) come on top of the list of movies proposed for said user.

<br/>
<h3>/ Collaborative Filtering - Model Based - Matrix Factorization /</h3>

As the last addon to this project a model based version of the movie recommender was added.
It is one of collaborative filtering techniques along with the memory based approach, but this time we use a model to get the
results. In this case we use Matrix Factorization which depends on building latency factor matrices and calculate the values inside
of these matrices so that they can reproduce the original ratings matrix and thus give information about the expected response to watching yet unseen movies and reduce memory used as only two small matrices are needed to store information instead of one matrix of huge size. The factors are tuned by iterating and correcting the values based on the obtained error value calculated as the sum of the squares of the differences between the expected and obtained values.
