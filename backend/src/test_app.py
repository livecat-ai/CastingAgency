import os
import unittest
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import setup_db, Actor, Movie, db

from app import create_app



class AppTestCase(unittest.TestCase):

    def setUp(self):
            """This class represents the test cases for Agency."""
    def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client
        database_path = os.environ['DATABASE_URL']
        self.app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        # ctx = self.app.app_context()
        # ctx.push()
        self.db = db
        self.db.init_app(self.app)
        with self.app.app_context():
            self.db.create_all()

        self.data = [
            {'name': 'Tom Hanks', 'age': 63, 'gender': 'm'}
            ]


    def setup_db(self, app):
        database_path = os.environ['TEST_DATABASE_URL']
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.db.app = app
        self.db.init_app(app)
        self.db.create_all()


    def tearDown(self):
        # pass
        # with self.app.app_context():
        #     self.db.session.remove()
        #     self.db.drop_all()
        self.db.session.remove()
        self.db.drop_all()

    # def test_actors(self):
    #     res = self.client().get('/')
    #     # data = json.loads(res)
    #     print(res)

    # def test_create_actor(self):
    #     new_book = {'name': 'Charlize Theron', 'age': 45, 'gender': 'f'}
    #     res = self.client().post('/actor/create', json=new_book)
    #     print()
    #     print(res)
    #     print()
    #     data = json.loads(res.data)
    #     self.asserEqual(res.status_code, 200)
    #     # self.asserEqual(data['success'], True)

    def test_get_specific_actor(self):
        id = 1
        res = self.client().get(f'/actor/{id}')
        data = json.loads(res.data)['actor']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id'], id)
        self.assertEqual(data['name'], 'Tom Hanks')

    def test_get_specific_actor_not_found(self):
        id = 2
        res = self.client().get(f'/actor/{id}')
        self.assertEqual(res.status_code, 404)


    




if __name__ == "__main__":
    unittest.main()

