import csv
import datetime as dt

#u.user: user id | age | gender | occupation | zip code
class User:
    def __init__(self, init_list):
        self.id = init_list[0]
        self.age = int(init_list[1])
        self.gender  =init_list[2]
        self.occupation = init_list[3]
        self.zip = init_list[4]

    def get_ratings(self, all_ratings):
        return [x for x in all_ratings if x.user == self.id]
#u.data: user id | item id | rating | timestamp
class Rating:
    def __init__(self, init_list):
        self.user = init_list[0]
        self.movie = init_list[1]
        self.rating = int(init_list[2])
        self.time = dt.datetime.fromtimestamp(int(init_list[3]))

#u.item:movie id | movie title | release date | video release date |
# IMDb URL | unknown | Action | Adventure | Animation |
# Children's | Comedy | Crime | Documentary | Drama | Fantasy |
# Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |
# Thriller | War | Western |

GENRES = ["unknown", "Action", "Adventure", "Animation",
    "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
    "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi",
    "Thriller", "War", "Western"]

class Movie:
    def __init__(self,init_list):
        self.id = init_list[0]
        self.title = init_list[1]
        try:
            self.release = dt.datetime.strptime(init_list[2],'%d-%b-%Y')
        except ValueError:
            self.release = None
        try:
            self.video = dt.datetime.strptime(init_list[3],'%d-%b-%Y')
        except ValueError:
            self.video = None
        self.IMDb = init_list[4]
        self.genres = {}
        for genre, value in zip(GENRES,init_list[5:25]):
            self.genres[genre] = int(value)

    def get_ratings(self, ratings_list):
        return [x for x in ratings_list if x.movie == self.id]

    def get_avg_rating(self, ratings_list):
        ratings = self.get_ratings(ratings_list)
        return sum([x.rating for x in ratings]) / len(ratings)

def get_title_by_id(movie_id, movies_list):
    movies = [x for x in movies_list if x.id == movie_id]
    if len(movies) == 1:
        return movies[0].title
    elif len(movies) == 0:
        return None
    else:
        raise ValueError('More than 1 movie with the id: {}.'.format(movie_id))

def read_file(filename, delim, constructor, number_of_items='all'):
    items = []
    with open(filename,'r') as f:
        reader = csv.reader(f, delimiter = delim)
        for number, row in enumerate(reader):
            items.append(constructor(row))
            if number_of_items == 'all':
                continue
            elif number >= number_of_items - 1:
                break
    return items

def read_movies(number_of_movies ='all', filename='ml-100k/u.item'):
    return read_file(filename,'|', Movie, number_of_movies)

def read_users(number_of_users='all', filename='ml-100k/u.user'):
    return read_file(filename, '|', User, number_of_users)

def read_ratings(number_of_ratings='all', filename='ml-100k/u.data'):
    return read_file(filename,'\t',Rating, number_of_ratings)

# read_movies(10)
# read_users(10)
# read_ratings(10)
