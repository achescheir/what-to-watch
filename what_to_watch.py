from movie_lib import *
import cProfile

library = MovieLibrary()
for x in library.get_top_popular_movies(20):
    print(library.movies[x].title,sum([y.rating for y in library.ratings_by_movie[x]])/len(library.ratings_by_movie[x]))


for x in library.get_popular_movies_for_user(library.users['25'],number_of_movies = 20):
    print(library.movies[x].title,sum([y.rating for y in library.ratings_by_movie[x]])/len(library.ratings_by_movie[x]))
