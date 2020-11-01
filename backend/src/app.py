import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']

app = Flask(__name__,template_folder='../../frontend/src/templates/')
app.config['SQLALCHEMY_DATABASE_URI'] = database_path
db = SQLAlchemy(app)


class Movies(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    releasedate = db.Column(db.Date, nullable=False)
    # actors = db.relationship('actors', backref='movie', lazy=True)

    def __repr__(self):
        return f'< Movies: {self.title}, {self.releasedate} >'


class Actors(db.Model):
    __tablename__ = "actors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    # movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    def __repr__(self):
        return f'< Actors: {self.name}, {self.age}, {self.gender} >'


db.create_all()

@app.route('/')
def index():
    return render_template('index.html', data=Movies.query.all())