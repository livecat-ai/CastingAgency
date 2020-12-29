import os

from datetime import date

from app import create_app
from models import db, setup_db, Actor, Movie, movie_cast


def add_actors():
    actors = [["Tom Hanks", 64, "m"],
              ["Charlize Theron", 45, "f"],
              ["Sigurney Weaver", 71, "f"],
              ['Noomi Rapace', 41,  'f'],
              ['Idris Elba', 48, 'm']]

    def add_new_actor(name, age, gender):
        query = Actor.query.filter(Actor.name == name).first()
        if query is None:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
    for actor in actors:
        add_new_actor(actor[0], actor[1], actor[2])


def add_movies():
    movies = [
                ["Prometheus", date(2012, 6, 8), []],
                ["Blade Runner", date(1982, 6, 25), []],
                ["Thelma and Louise", date(1991, 5, 24), []]
                ]

    def add_new_movie(title, date, actors=[]):
        query = Movie.query.filter(Movie.title == title).first()
        if query is None:
            movie = Movie(title=title, releasedate=date, actors=actors)
            movie.insert()
    for movie in movies:
        add_new_movie(movie[0], movie[1], movie[2])


def cast_movie():
    actors = Actor.query.filter(Actor.name.in_(
                                ['Charlize Theron', 'Noomi Rapace'])).all()
    movie = Movie.query.filter(Movie.title == 'Prometheus').first()
    movie.actors = actors
    movie.update()


def create_test_data():
    app = create_app()
    database_path = os.environ['TEST_DATABASE_URL']

    add_actors()
    add_movies()
    cast_movie()


if __name__ == '__main__':
    create_test_data()
