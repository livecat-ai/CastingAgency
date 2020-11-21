from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_migrate import Migrate
from flask_cors import CORS

from models import setup_db, Actor, Movie

ITEMS_PER_PAGE = 5

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, template_folder='../../frontend/src/templates/')
    db = setup_db(app)
    # migrate = Migrate(app, db)


    # app = Flask(__name__,template_folder='../../frontend/src/templates/')
    # db = setup_db(app)
    # migrate = Migrate(app, db)
    # db.create_all()

    CORS(app)

    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response

    '''
    Todo:
        - edit actor
        - delete actor
        - add movie
        - edit movie
        - delete movie
        - get specific movie
        - add project
    '''

    @app.route('/actor/create', methods=["POST"])
    def create_actor():
        # name = request.form.get('name')
        # age = int(request.form.get('age'))
        # gender = request.form.get('gender')
        # actor = Actor(name=name, age=age, gender=gender)
        # db.session.add(actor)
        # db.session.commit()
        return jsonify({
            'success': True
        })


    @app.route('/actors')
    def get_actors():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        formated_actors = [actor.format() for actor in Actor.query.all()]
        return jsonify({
            'success': True,
            'actors': formated_actors[start:end],
            'total_actors': len(formated_actors)
            })


    @app.route('/actor/<int:actor_id>', methods=['GET'])
    def get_specific_actor(actor_id):
        query = Actor.query.get(actor_id)
        if query == None:
            abort(404)

        return jsonify({
            'success': True,
            'actor': query.format()
        })


    @app.route('/')
    def index():
        for actor in Actor.query.all():
            print(actor)
        return render_template('index.html', data=Actor.query.all())


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error"
        }), 500

    return app