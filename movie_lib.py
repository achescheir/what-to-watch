import csv
import datetime as dt
import statistics as stats

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

    def get_ratings_value(self, ratings_list):
        return [x.rating for x in ratings_list if x.movie == self.id]

    def get_avg_rating(self, ratings_list):
        ratings = self.get_ratings_value(ratings_list)
        return stats.mean(ratings) #sum([x.rating for x in ratings]) / len(ratings)

    @staticmethod
    def get_title_by_id(movie_id, movies):
        return movies[movie_id]

class MovieLibrary:
    def __init__(self, ratings_file='ml-100k/u.data', movies_file='ml-100k/u.item', users_file='ml-100k/u.user'):
        self.ratings = self.read_ratings(filename=ratings_file)
        self.users = self.read_users(filename=users_file)
        self.movies = self.read_movies(filename=movies_file)
        self.ratings_by_movie = self.get_ratings_by_movie()
        self.ratings_by_user = self.get_ratings_by_user()

    @staticmethod
    def _read_items_file(filename, delim, constructor, number_of_items='all'):
        items = {}
        with open(filename,'r',encoding = "latin_1") as f:
            reader = csv.reader(f, delimiter = delim)
            for row in reader:
                this_item = constructor(row)
                items[this_item.id] = this_item
                if number_of_items == 'all':
                    continue
                elif len(items) >= number_of_items:
                    break
        return items

    @staticmethod
    def read_movies(number_of_movies ='all', filename='ml-100k/u.item'):
        return MovieLibrary._read_items_file(filename,'|',Movie, number_of_movies)

    @staticmethod
    def read_users(number_of_users='all', filename='ml-100k/u.user'):
        return MovieLibrary._read_items_file(filename,'|',User, number_of_users)

    @staticmethod
    def read_ratings(number_of_ratings='all', filename='ml-100k/u.data'):
        ratings = []
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter = '\t')
            for row in reader:
                ratings.append(Rating(row))
                if number_of_ratings == 'all':
                    continue
                elif len(ratings) >= number_of_ratings:
                    break
        return ratings

    def get_ratings_by_movie(self):
        ratings_by_movie ={}
        for rating in self.ratings:
            if rating.movie in ratings_by_movie:
                ratings_by_movie[rating.movie].append(rating)
            else:
                ratings_by_movie[rating.movie] = [rating]
        return ratings_by_movie

    def get_ratings_by_user(self):
        ratings_by_user ={}
        for rating in self.ratings:
            if rating.user in ratings_by_user:
                ratings_by_user[rating.user].append(rating)
            else:
                ratings_by_user[rating.user] = [rating]
        return ratings_by_user

    def get_movie_ids_sorted_by_avg_rating(self):
        movie_ids = list(self.ratings_by_movie.keys())
        movie_ids.sort(key = lambda x:stats.mean([y.rating for y in self.ratings_by_movie[x]]))
        return movie_ids

    def get_top_popular_movies(self, number_of_movies='all', min_ratings='1%'):
        if min_ratings == '1%':
            min_ratings = len(self.users)/100
        sorted_ids = self.get_movie_ids_sorted_by_avg_rating()
        sorted_ids.reverse()
        top_movie_ids = [x for x in sorted_ids if len(self.ratings_by_movie[x]) >= min_ratings]
        if number_of_movies == 'all':
            return top_movie_ids
        else:
            return top_movie_ids[:number_of_movies]

    def get_popular_movies_for_user(self, user, number_of_movies='all', min_ratings='1%'):
        top_movie_ids = self.get_top_popular_movies(min_ratings = min_ratings)
        user_ratings = [y.movie for y in self.ratings_by_user[user.id]]
        top_unseen_ids = [x for x in top_movie_ids if x not in user_ratings]
        if number_of_movies == 'all':
            return top_unseen_ids
        else:
            return top_unseen_ids[:number_of_movies]
# read_movies(10)
# read_users(10)
# read_ratings(10)
