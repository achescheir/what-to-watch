from movie_lib import *
import cProfile
import matplotlib.pyplot as plt

library = MovieLibrary()

print(library.get_similar_users('25'))
