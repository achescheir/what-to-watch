from nose.tools import raises
import datetime as dt
import movie_lib as ml

#u.user: user id | age | gender | occupation | zip code
test_user_row = ['12','28','F','other','06405']
#u.data: user id | item id | rating | timestamp
test_data_row = ['115','265','2','881171488']
#u.item:movie id | movie title | release date | video release date |
# IMDb URL | unknown | Action | Adventure | Animation |
# Children's | Comedy | Crime | Documentary | Drama | Fantasy |
# Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |
# Thriller | War | Western |
test_item_row = ['4','Get Shorty (1995)','01-Jan-1995','',
    'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
    '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0']

def test_user_constructor():
    test_user = ml.User(test_user_row)
    assert test_user.id == '12'
    assert test_user.age == 28
    assert test_user.gender == 'F'
    assert test_user.occupation == 'other'
    assert test_user.zip == '06405'

def test_rating_constructor():
    test_rating = ml.Rating(test_data_row)
    assert test_rating.user == '115'
    assert test_rating.movie == '265'
    assert test_rating.rating == 2
    assert test_rating.time == dt.datetime.fromtimestamp(881171488)

def test_movie_constructor():
    test_movie = ml.Movie(test_item_row)
    assert test_movie.id == '4'
    assert test_movie.title == 'Get Shorty (1995)'
    assert test_movie.release == dt.datetime.strptime('01-Jan-1995','%d-%b-%Y')
    assert test_movie.video == None
    assert test_movie.IMDb == 'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)'
    assert test_movie.genres == {"unknown":0, "Action":1, "Adventure":0, "Animation":0,
        "Children's":0, "Comedy":1, "Crime":0, "Documentary":0, "Drama":1,
        "Fantasy":0,"Film-Noir":0, "Horror":0, "Musical":0, "Mystery":0,
        "Romance":0, "Sci-Fi":0,"Thriller":0, "War":0, "Western":0}

test_movies = ml.MovieLibrary.read_movies(100)
test_users = ml.MovieLibrary.read_users(100)
test_ratings = ml.MovieLibrary.read_ratings(1000)

def test_user_get_ratings():
    test_ratings = [ml.Rating(['1','1','3','0']), ml.Rating(['1','2','3','0']),
        ml.Rating(['1','3','3','0']), ml.Rating(['2','1','3','0']),
        ml.Rating(['2','2','3','0']), ml.Rating(['3','1','3','0'])]
    test_user1 = ml.User(['1','24','M','technician','85711'])
    test_user2 = ml.User(['2','24','M','technician','85711'])
    test_user3 = ml.User(['3','24','M','technician','85711'])

    assert test_user1.get_ratings(test_ratings) == test_ratings[:3]
    assert test_user2.get_ratings(test_ratings) == test_ratings[3:5]
    assert test_user3.get_ratings(test_ratings) == test_ratings[5:]

def test_movie_get_ratings():
    test_ratings = [ml.Rating(['1','1','3','0']), ml.Rating(['1','2','3','0']),
        ml.Rating(['1','3','3','0']), ml.Rating(['2','1','3','0']),
        ml.Rating(['2','2','3','0']), ml.Rating(['3','1','3','0'])]
    test_movie1 = ml.Movie(['1','Get Shorty (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movie2 = ml.Movie(['2','Get Shorty 2 (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movie3 = ml.Movie(['3','Get Shorty 3 (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])

    assert test_movie1.get_ratings(test_ratings) == [test_ratings[0],test_ratings[3],test_ratings[5]]
    assert test_movie2.get_ratings(test_ratings) == [test_ratings[1],test_ratings[4]]
    assert test_movie3.get_ratings(test_ratings) == [test_ratings[2]]

def test_movie_get_avg_rating():
    test_ratings = [ml.Rating(['1','1','1','0']), ml.Rating(['1','2','1','0']),
        ml.Rating(['1','3','4','0']), ml.Rating(['2','1','2','0']),
        ml.Rating(['2','2','5','0']), ml.Rating(['3','1','3','0'])]
    test_movie1 = ml.Movie(['1','Get Shorty (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movie2 = ml.Movie(['2','Get Shorty 2 (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movie3 = ml.Movie(['3','Get Shorty 3 (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])

    assert test_movie1.get_avg_rating(test_ratings) == 2
    assert test_movie2.get_avg_rating(test_ratings) == 3
    assert test_movie3.get_avg_rating(test_ratings) == 4

def test_get_title_by_id():
    test_movie1 = ml.Movie(['1','Get Shorty (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movie2 = ml.Movie(['2','Get Shorty 2 (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movie3 = ml.Movie(['3','Get Shorty 3 (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movies = [test_movie1, test_movie2, test_movie3]
    assert ml.Movie.get_title_by_id('1', test_movies) == 'Get Shorty (1995)'
    assert ml.Movie.get_title_by_id('2', test_movies) == 'Get Shorty 2 (1995)'
    assert ml.Movie.get_title_by_id('3', test_movies) == 'Get Shorty 3 (1995)'

@raises(ValueError)
def test_get_title_by_id_duplicate_entry():
    test_movie1 = ml.Movie(['1','Get Shorty (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movie2 = ml.Movie(['2','Get Shorty 2 (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movie3 = ml.Movie(['3','Get Shorty 3 (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movies = [test_movie1, test_movie1, test_movie2, test_movie3]
    ml.Movie.get_title_by_id('1',test_movies)

@raises(ValueError)
def test_get_title_by_id_duplicate_id():
    test_movie1 = ml.Movie(['1','Get Shorty (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movie2 = ml.Movie(['1','Get Shorty 2 (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movie3 = ml.Movie(['3','Get Shorty 3 (1995)','01-Jan-1995','',
        'http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)','0','1','0','0',
        '0','1','0','0','1','0','0','0','0','0','0','0','0','0','0'])
    test_movies = [test_movie1, test_movie2, test_movie3]
    ml.Movie.get_title_by_id('1',test_movies)

def test_movielib():
    ml.MovieLibrary()
