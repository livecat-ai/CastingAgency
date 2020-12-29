import os
import unittest
import json
from datetime import date

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import setup_db, Actor, Movie, db

from app import create_app, is_valid_date_string, string_to_datetime
import jwt


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        # Uncomment this while connecting to heroku
        # self.database_path = "postgres://ahqolbipadtbpj:
        #                       8166ebc8ce23e355a963e79e074c28775
        #                       b189944b6935e1a3a2278b906fa4882@
        #                       ec2-3-208-50-226.compute-1.
        #                       amazonaws.com:5432/dbo69r1cnn6k5m"
        self.app = create_app(test_config=True)
        self.client = self.app.test_client
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.setup_db()
        self.add_actors()
        self.add_movies()
        self.add_productions()

    def setup_db(self):
        self.db.app = self.app
        self.db.init_app(self.app)
        self.db.create_all()

    def tearDown(self):
        pass

    def add_actors(self):
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

    def delete_all_actors(self):
        Actor.query.delete()
        self.db.session.commit()

    def add_movies(self):
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

    def delete_all_movies(self):
        Movie.query.delete()
        self.db.session.commit()

    def add_productions(self):
        actors = Actor.query.filter(Actor.name.in_([
                                    'Charlize Theron',
                                    'Noomi Rapace'
                                    ])).all()
        movie = Movie.query.filter(Movie.title == 'Prometheus').first()
        movie.actors = actors
        movie.update()

    # ---------------------------------
    # Test - All users
    # Run tests for endpoints authorized for all users
    # ---------------------------------

    def test_get_actors(self):
        for user in jwt.casting_assistant_and_above:
            header = {'Authorization': 'Bearer ' + user}
            res = self.client().get('/actors?page=1',
                                    content_type='application/json',
                                    headers=header)
            print(res)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(len(data['actors']))
            self.assertTrue(data['total_actors'])

    def test_get_actors_not_found(self):
        for user in jwt.casting_assistant_and_above:
            header = {'Authorization': 'Bearer ' + user}
            res = self.client().get('/actors?page=1000',
                                    content_type='application/json',
                                    headers=header)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    def test_get_movies(self):
        for user in jwt.casting_assistant_and_above:
            header = {'Authorization': 'Bearer ' + user}
            res = self.client().get('/movies?page=1',
                                    content_type='application/json',
                                    headers=header)
            data = json.loads(res.data)
            # print(res)
            # print(data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(len(data['movies']))
            self.assertTrue(data['total_movies'])

    def test_get_movies_not_found(self):
        for user in jwt.casting_assistant_and_above:
            header = {'Authorization': 'Bearer ' + user}
            res = self.client().get('/movies?page=1000',
                                    content_type='application/json',
                                    headers=header)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    # def test_search_actors(self):
    #     search_item =  {'name': 'char'}
    #     res = self.client().post(f'/actors/search',
    #                              data=json.dumps(search_item),
    #                              content_type='application/json')
    #     data = json.loads(res.data)
    #     # print(data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertIn(search_item['name'], data['actors'][0]['name'].lower())

    # def test_get_specific_actor(self):
    #     # get details of first row in db
    #     actor = Actor.query.first()
    #     id = actor.id
    #     name = actor.name
    #     # send get request
    #     res = self.client().get(f'/actors/{id}')
    #     data = json.loads(res.data)
    #     # run tests
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['actor']['id'], id)
    #     self.assertEqual(data['actor']['name'], name)

    # def test_get_specific_actor_not_found(self):
    #     # set id to none existant row
    #     id = get_last_item_in_db(Actor).id + 100
    #     #  send request
    #     res = self.client().get(f'/actors/{id}')
    #     data = json.loads(res.data)
    #     # run tests
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)

    # ---------------------------------
    # Test - Casting Director
    # Run tests for endpoints authorized for Casting Directors or above
    # ---------------------------------

    def test_add_new_actor(self):
        # send put request for id
        for user in jwt.casting_director_and_above:
            header = {'Authorization': 'Bearer ' + user}
            new_actor = {'name': 'Colin Farrel', 'age': 44, 'gender': 'm'}
            res = self.client().post(f'/actors', data=json.dumps(new_actor),
                                     content_type='application/json',
                                     headers=header)
            data = json.loads(res.data)
            # query the updated id so we can check it worked
            actor = get_last_item_in_db(Actor)
            # run tests
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(actor.name, new_actor['name'])
            self.assertEqual(actor.age, new_actor['age'])
            self.assertEqual(actor.gender, new_actor['gender'])

    def test_add_new_actor_invalid(self):
        for user in jwt.casting_director_and_above:
            header = {'Authorization': 'Bearer ' + user}
            new_actor = {'name': 3, 'age': '3.14', 'gender': 0}
            res = self.client().post(f'/actors', data=json.dumps(new_actor),
                                     content_type='application/json',
                                     headers=header)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        for user in jwt.casting_director_and_above:
            header = {'Authorization': 'Bearer ' + user}
            # set id to first existing row
            # id = Actor.query.first().id
            query = get_last_item_in_db(Actor)
            id = query.id
            # send request to delete id
            res = self.client().delete(f'/actors/{id}', headers=header)
            data = json.loads(res.data)
            # query the deleted id so we can check it doesn't exist anymore
            actor = Actor.query.get(id)
            # run tests
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], id)
            self.assertTrue(data['total_actors'])
            self.assertTrue(len(data['actors']))
            self.assertEqual(actor, None)

    def test_delete_actor_not_found(self):
        for user in jwt.casting_director_and_above:
            header = {'Authorization': 'Bearer ' + user}
            # set id to first existing row
            id = get_last_item_in_db(Actor).id + 100
            # send request to delete id
            res = self.client().delete(f'/actors/{id}', headers=header)
            data = json.loads(res.data)
            # run tests
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    def test_cast_movie(self):
        for user in jwt.casting_director_and_above:
            header = {'Authorization': 'Bearer ' + user}
            # Setup
            movie_title = 'Prometheus'
            actor_name = 'Idris Elba'
            movie = Movie.query.filter(Movie.title.ilike(
                                       f'{movie_title}')
                                       ).first()
            movie_id = movie.id
            actor_id = Actor.query.filter(Actor.name.ilike(
                                          f'{actor_name}')
                                          ).first().id
            res = self.client().patch(f'movies/cast/{movie_id}',
                                      data=json.dumps(dict(id=f'{actor_id}')),
                                      content_type='application/json',
                                      headers=header)
            data = json.loads(res.data)
            # Tests
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            actor_names = [actor['name'] for actor
                           in data['production']['actors']]
            self.assertIn(actor_name, actor_names)
            # Reset database
            movie = Movie.query.filter(Movie.title.ilike(
                                       f'{movie_title}')).first()
            movie.actors = Actor.query.filter(
                                              Actor.name.in_(
                                                [
                                                    'Charlize Theron',
                                                    'Noomi Rapace'
                                                ]
                                              )).all()
            movie.update()

    def test_cast_movie_not_found(self):
        for user in jwt.casting_director_and_above:
            header = {'Authorization': 'Bearer ' + user}
            movie_title = 'Breakdance 2: Electric Boogaloo'
            actor_name = 'Tom Hanks'
            actor_id = Actor.query.filter(Actor.name.ilike(
                                          f'{actor_name}')
                                          ).first().id
            movie_id = 1000
            res = self.client().patch(f'movies/cast/{movie_id}',
                                      data=json.dumps(dict(id=f'{actor_id}')),
                                      content_type='application/json',
                                      headers=header)
            # Tests
            self.assertEqual(res.status_code, 404)

    # def test_edit_actor_age(self):
    #     # set id to first existing row
    #     query = Actor.query.first()
    #     id = query.id
    #     original_age = query.age
    #     new_age = original_age + 1
    #     # send put request for id
    #     res = self.client().patch(f'/actors/{id}', data=dict(age=new_age))
    #     data = json.loads(res.data)
    #     # query the updated id so we can check it worked
    #     actor = Actor.query.get(id)
    #     # run tests
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(actor.age, new_age)

    # def test_edit_age_actor_not_found(self):
        # # set id to first existing row
        # id = get_last_item_in_db(Actor).id + 100
        # # send request to delete id
        # res = self.client().patch(f'/actors/{id}', data=dict(age=999))
        # data = json.loads(res.data)
        # # run tests
        # self.assertEqual(res.status_code, 404)
        # self.assertEqual(data['success'], False)

    # def test_cast_actors(self):
    #     actors = Actor.query.filter(Actor.name.in_(
    #                               ['Charlize Theron',
    #                                'Noomi Rapace'])).all()
    #     movie = Movie.query.filter(Movie.title == 'Prometheus').first()
    #     res = self.client().put(f'/production/{id}', data=actor_id)

    # ---------------------------------
    # Test - Exec Producer
    # Run tests for endpoints authorized for Exec Producers or above
    # ---------------------------------

    def test_add_new_movie(self):
        for user in jwt.exec_producer:
            header = {'Authorization': 'Bearer ' + user}
            # send put request for id
            new_movie = {'title': 'Gladiator', 'releasedate': '2000-05-12'}
            res = self.client().post(f'/movies/create',
                                     data=json.dumps(new_movie),
                                     content_type='application/json',
                                     headers=header)
            data = json.loads(res.data)
            # query the updated id so we can check it worked
            movie = get_last_item_in_db(Movie)
            # print(f'adding movie {movie}')
            # run tests
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(movie.title, new_movie['title'])
            self.assertEqual(movie.releasedate.strftime('%Y-%m-%d'),
                             new_movie['releasedate'])

    def test_add_new_movie_invalid(self):
        for user in jwt.exec_producer:
            header = {'Authorization': 'Bearer ' + user}
            new_movie = {'title': 3, 'releasedate': '3.14'}
            res = self.client().post(f'/movies/create',
                                     data=json.dumps(new_movie),
                                     content_type='application/json',
                                     headers=header)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 400)
            self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        for user in jwt.exec_producer:
            header = {'Authorization': 'Bearer ' + user}
            # set id to first existing row
            # id = Movie.query.first().id
            query = get_last_item_in_db(Movie)
            id = query.id
            # print(f'deleting movie {query}')
            # send request to delete id
            res = self.client().delete(f'/movies/{id}', headers=header)
            data = json.loads(res.data)
            # query the deleted id so we can check it doesn't exist anymore
            movie = Movie.query.get(id)
            # run tests
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], id)
            self.assertTrue(data['total_movies'])
            self.assertTrue(len(data['movies']))
            self.assertEqual(movie, None)

    def test_delete_movie_not_found(self):
        for user in jwt.exec_producer:
            header = {'Authorization': 'Bearer ' + user}
            # set id to first existing row
            id = get_last_item_in_db(Movie).id + 100
            # send request to delete id
            res = self.client().delete(f'/movies/{id}', headers=header)
            data = json.loads(res.data)
            # run tests
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    # def test_is_valid_date_string(self):
    #     date_string = '2000-05-12'
    #     self.assertTrue(is_valid_date_string(date_string))

    # def test_search_movies(self):
    #     search_item =  {'title': 'run'}
    #     res = self.client().post(f'/movies/search',
    #                   data=json.dumps(search_item),
    #                   content_type='application/json')
    #     data = json.loads(res.data)
    #     print(data)
    #     # print(data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertIn(search_item['title'],
    #                   data['movies'][0]['title'].lower())

    # def test_get_specific_movie(self):
    #     # get details of first row in db
    #     movie = Movie.query.first()
    #     id = movie.id
    #     title = movie.title
    #     # send get request
    #     res = self.client().get(f'/movies/{id}')
    #     data = json.loads(res.data)
    #     # print(data)
    #     # print(f'finding {movie}')
    #     # run tests
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['movie']['id'], id)
    #     self.assertEqual(data['movie']['title'], title)

    # def test_get_specific_movie_not_found(self):
    #     # set id to none existant row
    #     id = get_last_item_in_db(Movie).id + 100
    #     #  send request
    #     res = self.client().get(f'/movies/{id}')
    #     data = json.loads(res.data)
    #     # run tests
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)

    # def test_edit_movie_releasedate(self):
    #     # set id to first existing row
    #     id = 1
    #     query = Movie.query.get(id)
    #     original_date = query.releasedate
    #     new_date = date(2020, 7, 1)
    #     # send put request for id
    #     res = self.client().patch(f'/movies/{id}',
    #                       data=dict(releasedate=new_date))
    #     data = json.loads(res.data)
    #     # query the updated id so we can check it worked
    #     movie = Movie.query.get(id)
    #     # run tests
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(movie.releasedate, new_date)
    #     movie.releasedate = original_date
    #     movie.update()

    # def test_edit_new_movie_not_found(self):
    #     # set id to first existing row
    #     id = get_last_item_in_db(Movie).id + 100
    #     # send request to delete id
    #     res = self.client().patch(f'/movies/{id}',
    #                  data=dict(releasedate=date(1066, 10, 14)))
    #     data = json.loads(res.data)
    #     # run tests
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
# ---------------------------------
# Global helper functions
# ---------------------------------


def get_last_item_in_db(db_table_object):
    table = db_table_object
    return table.query.order_by(table.id.desc()).first()


if __name__ == "__main__":
    unittest.main()
