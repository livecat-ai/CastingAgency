import os
import sys

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_migrate import Migrate
from flask_cors import CORS


from models import setup_db, db, Actor, Movie

#--- Uncomment below to disable Auth ---
# from no_auth import requires_auth, AuthError

#--- Uncomment below to enable Auth ---
from auth import requires_auth, AuthError



ITEMS_PER_PAGE = 8

#----------------------------------------------
# Helper functions
#----------------------------------------------
def paginate(query, request):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    return [item.format() for item in query[start: end]]

def is_valid_date_string(date_string):
    result = True
    try:
        _ = string_to_datetime(date_string)
    except ValueError:
        result = False
    return result

def string_to_datetime(date_string, fmt = '%Y-%m-%d'):
    return datetime.strptime(date_string, fmt)

def is_string_valid_integer(int_string):
    out = True
    # Check if it's even a number
    try:
        num = float(int_string)
    except:
        return False
    out = True
    if (int(num) - num) != 0:
        out = False
    return out


#----------------------------------------------
# Create App
#----------------------------------------------
def create_app(test_config=False):
    # create and configure the app
    if test_config == True:
        database_path = os.environ['TEST_DATABASE_URL']
    elif test_config == False:
        # database_path = os.environ['DATABASE_URL']
        database_path = os.environ['TEST_DATABASE_URL']

    app = Flask(__name__, template_folder='../../frontend/src/templates/')
    setup_db(app, database_path = database_path)
 
    CORS(app)
  
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response



    #--------------------------------------------------
    # Controlers
    #--------------------------------------------------



    #--------------------------------------------------
    # Actor
    #--------------------------------------------------
    @app.route('/actors', methods=["GET"])
    @requires_auth('get:actors')
    def get_actors(jwt):
        query = Actor.query.all()
        total_actors = len(query)
        actors = paginate(query, request)
        if len(actors) == 0:
            abort(404)
        # formated_actors = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': actors,
            'total_actors': total_actors
            })


    # @app.route('/actors/<int:actor_id>', methods=['GET'])
    # @requires_auth('get:actors')
    # def get_specific_actor(jwt, actor_id):
    #     query = Actor.query.get(actor_id)
    #     if query == None:
    #         abort(404)
    #     return jsonify({
    #         'success': True,
    #         'actor': query.format()
    #     })

    @app.route('/actors', methods=["POST"])
    @requires_auth('post:actors')
    def create_actor(jwt):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            new_actors = Actor.query.filter(Actor.name==name).all() # There might be more than one with the same name
            actor_id = max([actor.id for actor in new_actors])
            query = Actor.query.order_by(Actor.id).all()
            actors = paginate(query, request)
        except:
            db.session.rollback()
            db.session.close()
            abort(422)
        return jsonify({
            'success': True,
            'created': actor_id,
            'actors': actors,
            'total_actors': len(Actor.query.all())
        })


    # @app.route('/actors/search', methods=['POST'])
    # def search_actors():
    #     body = request.get_json()
    #     search_term = body.get('name', None)
    #     query = Actor.query.filter(Actor.name.ilike(f'%{search_term}%')).all()
    #     actors = paginate(query, request)
    #     return jsonify({
    #         'success': True,
    #         'count': len(actors),
    #         'actors': actors
    #     })


    # @app.route('/actors/<int:actor_id>', methods=["PATCH"])
    # def edit_actor(actor_id):
    #     age = int(request.form.get('age'))
    #     actor = Actor.query.get(actor_id)
    #     if actor == None:
    #         abort(404)
    #     # print(actor.format())
    #     # print(f'editing {actor.name}')
    #     # print(f"old age: {actor.age}")
    #     # print(f"new age: {age}")
    #     actor.age = age
    #     actor.update()
    #     return jsonify({
    #         'success': True,
    #         'age': age
    #     })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors') 
    def delete_specific_actor(jwt, actor_id):
        actor = Actor.query.get(actor_id)
        if actor == None:
            abort(404)
        # print(actor.format())
        print(f'deleted {actor.name}')
        actor.delete()
        query = Actor.query.all()
        total_actors = len(query)
        actors = paginate(query, request)
        # formated_actors = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'deleted': actor_id,
            'total_actors': total_actors,
            'actors': actors
        })

    # #--------------------------------------------------
    # # Movie
    # #--------------------------------------------------
    @app.route('/movies', methods = ['GET'])
    @requires_auth('get:movies') 
    def get_movies(jwt):
        query = Movie.query.all()
        total_movies = len(query)
        movies = paginate(query, request)
        if len(movies) == 0:
            abort(404)
        # formated_movies = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': movies,
            'total_movies': total_movies
            })

    # @app.route('/movies/<int:movie_id>', methods=['GET'])
    # def get_specific_movie(movie_id):
    #     query = Movie.query.get(movie_id)
    #     if query == None:
    #         abort(404)
    #     return jsonify({
    #         'success': True,
    #         'movie': query.format()
    #     })

    # @app.route('/movies/search', methods=['POST'])
    # def search_movies():
    #     body = request.get_json()
    #     search_term = body.get('title', None)
    #     print(search_term)
    #     query = Movie.query.filter(Movie.title.ilike(f'%{search_term}%')).all()
    #     movies = paginate(query, request)
    #     return jsonify({
    #         'success': True,
    #         'count': len(movies),
    #         'movies': movies
    #     })

    @app.route('/movies/create', methods=["POST"])
    @requires_auth('post:movies') 
    def create_movie(jwt):
        # title = request.form.get('title')
        # releasedate = request.form.get('releasedate')
        body = request.get_json()
        title = body.get('title', None)
        releasedate = body.get('releasedate', None)
        if not is_valid_date_string(releasedate):
            abort(400)
        movie = Movie(title=title, releasedate=string_to_datetime(releasedate))
        movie.insert()
        return jsonify({
            'success': True
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies') 
    def delete_specific_movie(jwt, movie_id):
        movie = Movie.query.get(movie_id)
        if movie == None:
            abort(404)
        # print(movie.format())
        # print(f'deleted {movie.name}')
        movie.delete()
        query = Movie.query.all()
        total_movies = len(query)
        movies = paginate(query, request)
        # formated_movies = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'deleted': movie_id,
            'total_movies': total_movies,
            'movies': movies
        })

    # @app.route('/movies/<int:movie_id>', methods=["PATCH"])
    # def edit_movie(movie_id):
    #     releasedate = request.form.get('releasedate')
    #     if not is_valid_date_string(releasedate):
    #         abort(400)
    #     movie = Movie.query.get(movie_id)
    #     if movie == None:
    #         abort(404)
    #     # print(actor.format())
    #     # print(f'editing {actor.name}')
    #     # print(f"old age: {actor.age}")
    #     # print(f"new age: {age}")
    #     # print(releasedate)
    #     movie.releasedate = datetime.strptime(releasedate, '%Y-%m-%d')
    #     movie.update()
    #     return jsonify({
    #         'success': True,
    #         'releasedate': releasedate
    #     })

    # #--------------------------------------------------
    # # Production
    # #--------------------------------------------------

    @app.route('/movies/cast/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies') 
    def cast_movie(jwt, movie_id):
        actor_id = request.form.get('id')
        actor = Actor.query.get(actor_id)
        movie = Movie.query.get(movie_id)
        if (movie == None) or (actor == None):
            abort(404)
        movie.actors.append(actor)
        movie.update()
        # print(f'Movie: {movie}')
        # print('movie')
        return jsonify({
            'success': True,
            'production': Movie.query.get(movie_id).format()
        })


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbiden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbiden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def mothod_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server error"
        }), 500


    return app

# create app
app = create_app()

if __name__ == '__main__':
    app.run()