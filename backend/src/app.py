import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database_path = os.environ['DATABASE_URL']

app = Flask(__name__,template_folder='../../frontend/src/templates/')
app.config['SQLALCHEMY_DATABASE_URI'] = database_path
db = SQLAlchemy(app)


migrate = Migrate(app, db)
movie_cast = db.Table('movie_cast',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True)
    )

class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    # releasedate = db.Column(db.Date, nullable=False)
    actors = db.relationship('Actor', secondary=movie_cast,
        backref=db.backref('movies', lazy=True))

    # def __init__(self, title, release_date):
    #     self.title = title
    #     self.releasedate = release_date

    # def __repr__(self):
    #     return f'< Movies: {self.title}, {self.releasedate} >'

    def __repr__(self):
        return f'< Movies: {self.title} >'


class Actor(db.Model):
    __tablename__ = "actor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # age = db.Column(db.Integer, nullable=False)
    # gender = db.Column(db.String, nullable=False)
    # movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    # def __init__(self, name, age, gender, movie_id):
    #     self.name = name
    #     self.age = age
    #     self.gender = gender
    #     self.movie_id = movie_id

    # def __repr__(self):
    #     return f'< Actors: {self.name}, {self.age}, {self.gender} >'

    def __repr__(self):
        return f'< Actors: {self.name}>'


# db.create_all()

@app.route('/')
def index():
    return render_template('index.html', data=Movies.query.all())