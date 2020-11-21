import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

database_path = os.environ['DATABASE_URL']


def setup_db(app, database_path = database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    return db
    
    
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


class Actor(db.Model):
    __tablename__ = "actor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    # movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=True)

    def __repr__(self):
        return f'< Actors: {self.name}, {self.age}, {self.gender} >'

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }

# db.create_all()