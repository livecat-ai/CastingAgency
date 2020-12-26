import os
import sys

from flask import abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def setup_db(app, database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()  
    
movie_cast = db.Table('movie_cast',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True)
    )

class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    releasedate = db.Column(db.Date, nullable=False)
    actors = db.relationship('Actor', secondary=movie_cast,
        backref=db.backref('movies', lazy=True))

    def __repr__(self):
        return f'< Movie: {self.title} >'

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.close()
            print(sys.exc_info())
            abort(422)

    def update(self):
        error = None
        try:
            db.session.commit()
        except:
            db.session.rollback()
            error = 422
            print(sys.exc_info())
        finally:
            db.session.close()
        if error != None:
            abort(error)
        
    def delete(self):
        error = None
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            error = 422
            print(sys.exc_info())
        finally:
            db.session.close()
        if error != None:
            abort(error)

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "releasedate": self.releasedate,
            "actors": [actor.format() for actor in self.actors]
        }



class Actor(db.Model):
    __tablename__ = "actor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'< Actors: {self.name}, {self.age}, {self.gender} >'

    def insert(self):
        # error = None
        # try:
        #     db.session.add(self)
        #     db.session.commit()
        # except:
        #     db.session.rollback()
        #     error = 422
        #     print(sys.exc_info())
        # finally:
        #     db.session.close()
        # if error != None:
        #     abort(error)
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        error = None
        try:
            db.session.commit()
        except:
            db.session.rollback()
            error = 422
            print(sys.exc_info())
        finally:
            db.session.close()
        if error != None:
            abort(error)
        
    def delete(self):
        error = None
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            error = 422
            print(sys.exc_info())
        finally:
            db.session.close()
        if error != None:
            abort(error)


    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }



