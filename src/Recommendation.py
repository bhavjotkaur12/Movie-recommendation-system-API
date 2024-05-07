import pandas as pd
import numpy as np

def load_data():
    # Loading dataset into dataframes
    links_df = pd.read_csv('Data/links.csv')
    movies_df = pd.read_csv('Data/movies.csv')
    ratings_df = pd.read_csv('Data/ratings.csv')
    tags_df = pd.read_csv('Data/tags.csv')

    # checking for missing values and data types
    print(movies_df.info())
    print(ratings_df.info())
    print(tags_df.info())
    print(links_df.info())


    # Handling missing values: Removing 'tmdbId' since not crucial for recommendation
    links_df.drop('tmdbId', axis=1, inplace=True)
    
    # Removing irrelevant timestamp data
    ratings_df.drop('timestamp', axis=1, inplace=True)
    tags_df.drop('timestamp', axis=1, inplace=True)

    # Removing duplicates if any
    movies_df.drop_duplicates(subset='movieId', keep='first', inplace=True)
    ratings_df.drop_duplicates(subset=['userId', 'movieId'], keep='first', inplace=True)
    tags_df.drop_duplicates(subset=['userId', 'movieId', 'tag'], keep='first', inplace=True)

    # Printing statistics of movie ratings
    print('Basic statistics of movie ratings')
    print(ratings_df['rating'].describe())

    # Popular movie stats
    print('Popular movie stats')
    movie_stats = ratings_df.groupby('movieId').agg({'rating': ['mean', 'count']})
    popular_movies = movie_stats[movie_stats['rating']['count'] > 50].sort_values(by=('rating', 'mean'), ascending=False)
    print(popular_movies.head())

    # Merging movies_df with aggregated ratings data
    movie_stats = ratings_df.groupby('movieId').agg(
        average_rating=pd.NamedAgg(column='rating', aggfunc='mean'),
        rating_count=pd.NamedAgg(column='rating', aggfunc='count')
    )
    movies_with_ratings = pd.merge(movies_df, movie_stats, on='movieId', how='left')

    return movies_with_ratings

def recommend_movies(movies_with_ratings, genres, min_rating=3.5, count_threshold=50):
    """
    Recommend movies based on preferred genres and a minimum rating threshold.
    """
    mask = (movies_with_ratings['genres'].str.contains('|'.join(genres))) & \
           (movies_with_ratings['average_rating'] >= min_rating) & \
           (movies_with_ratings['rating_count'] >= count_threshold)
    recommendations = movies_with_ratings[mask].sort_values(by='average_rating', ascending=False)
    return recommendations

# Load data and make recommendations
movies_with_ratings = load_data()

# Example: Recommend Action or Crime movies with high ratings
recommended_movies = recommend_movies(movies_with_ratings, ['Action', 'Crime'], min_rating=4.2)
print('Recommended movies:')
print(recommended_movies[['title', 'average_rating', 'rating_count', 'genres']])
