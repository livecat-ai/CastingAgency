import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks')
def get_drinks(jwt):
    # @requires_auth('get:drinks')
    # def get_drinks(jwt):
    # @TODO unpack the request header
 #   print(jwt)
    drinks = [drink.short() for drink in Drink.query.all()]
    print(drinks)
    body = {
        'success': True,
        'drinks': drinks
    }
    return jsonify(body)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    # @TODO unpack the request header
    print(jwt)
    drinks = [drink.long() for drink in Drink.query.all()]
    print(drinks)
    body = {
        'success': True,
        'drinks': drinks
    }
    return jsonify(body)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    # @TODO unpack the request header
    # print(jwt)
    req = request.get_json()
    title = req['title']
    recipe = req['recipe']
    query = Drink.query.filter(Drink.title == title).first()
    if query:
        abort(422)
    drink = Drink(title=title, recipe=json.dumps(recipe))
    drink.insert()
    body = {
        'success': True,
        'drinks': req
    }
    return jsonify(body)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(jwt, id):
    # @TODO unpack the request header
    print(jwt)

    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink == None: abort(404)

    req = request.get_json()
    print(f'req:{req}')
    if ("title" in req) and ("recipe" in req):
        title = req['title']
        recipe = req['recipe']
    else:
        abort(400)

    try:
        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()
    except:
        abort(500)
    
    body = {
        'success': True,
        'drinks': [drink.long()]
    }
    return jsonify(body)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt, id):
    # @TODO unpack the request header
    print(jwt)
    drink = Drink.query.get(id)
    if drink:
        drink.delete()
    else:
        abort(404)
    body = {
        'success': True,
        'delete': id
    }
    return jsonify(body)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(400)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(401)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "request is forbiden"
    }), 403


@app.errorhandler(500)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500
