from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import TV
import random

tmdb = TMDb()
tmdb.api_key = 'TMDB_API_KEY'

# error code - 0. couldn't find movie
# erroe code 1. couldn't find similar movie


def get_recommendation():
    movie = Movie()
    recommendation = random.choice(movie.popular())
    return {"title": recommendation.title, "overview": recommendation.overview, "vote": str(recommendation.vote_average)+"/10", "poster": "https://image.tmdb.org/t/p/w1280"+recommendation.poster_path}


def get_similar(string):
    movie = Movie()
    movies = movie.search(string)
    if len(movies) == 0:
        return 0
    similar_movies = movie.similar(random.choice(movies).id)
    if len(similar_movies) == 0:
        return 1
    similar_movie = random.choice(similar_movies)
    return {"title": similar_movie.title, "overview": similar_movie.overview, "vote": str(similar_movie.vote_average)+"/10", "poster": "https://image.tmdb.org/t/p/w1280"+similar_movie.poster_path}


if __name__ == "__main__":
    print(get_recommendation())
    print(get_similar('ad astra'))
