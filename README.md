# Movie-Recommendation-App

The purpose of this program is to present some techniques of movie recommendation systems used, among others, by streaming services.
<br/><br/>

/ Collaborative Filtering - Memory Based - Pearson Correlation /

In the first version of the program, a collaborative filtering technique is implemented using similarities between users to find people that rate movies alike and thus movies watched by one person will probably be rated high by another person if the correlation score between these two users is high. The similarity between users (friends) was calculated using Pearson Correlation score which is one of the memory based methods. 

<br/>
/ Content Filtering - Item Based - Dot product of two matrices /

In the second version of the program, a content filtering technique is used which means that the movie recommendation list is calculated based on the correlation between items features - in this case the movie genres. To calculate the correlation first it is necessary to calculate the user's movie taste (a data structure containing favorite movie genres) based on the ratings given by said user to already watched movies that have some features to be identified (e.g. movie genre).
Then the result values are used to compare them with yet unwatched movies and so the movies that have the highest score (have the most features appreciated by the user) come on top of the list of movies proposed for said user.
