
# CastinAgency API Backend

## About
The CastingAgency app is used to store details of both actors and movies. In addition actors can be cast in movies.
A user can send a post requests to add both actors and movies along as well as retrieve information about registered actors and movies.
Additionally actors can be assigned to movies and both movies and actors can be removed from the database.

The warranty tracker app is used to store products and keep track of the warranty dates associated with the products.
A user can send a post request with the product name, date purchased, and warranty end date in order to store these values. The user can also
retrieve these products and their details to check if a product's warranty has expired or not. Further, the user can update the product details and
also delete the product by sending requests to the appropriate endpoints.

The endpoints and how to send requests to these endpoints for products and items are described in the 'Endpoint Library' section of the README.

All endpoints need to be tested using curl or postman since there is no frontend for the app yet.


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

In the warranty-tracker directory, run the following to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

To run the server, execute:
```
source setup.sh
python3 app.py
```
We can now also open the application via Heroku using the URL:
https://casting-jal.herokuapp.com/

The live application can only be used to generate tokens via Auth0, the endpoints have to be tested using curl or Postman 
using the token since I did not build a frontend for the application.


## DATA MODELING:
#### models.py
The schema for the database and helper methods to simplify API behavior are in models.py:
- There are three tables created: Movie, Actor, and movie_cast
- The Movie table is used to add new movies, and also retrieve these movies.
- The Actor table is used to add new actors, and also retrieve these actors.
- The movie_cast is an association table storing both actor_id and movie_id. It provides a way to associate actors with movies
The Movie and Actor tables have an insert, update, delete, and format helper functions.

## API ARCHITECTURE AND TESTING
### Endpoint Library

@app.errorhandler decorators were used to format error responses as JSON objects. Custom @requires_auth decorator were used for Authorization based
on roles of the user. Three roles are assigned to this API: 'exec_producer' and 'casting_direcotor' and 'casting_assistant'. All roles are already pre-assigned to certain users.

#### Roles:
## Casting Assistant
- Can view actors and movies
A sample token for this role is stored in the AUTH_CASTING_ASSISTANT environment variable

## Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies
A sample token for this role is stored in the AUTH_CASTING_DIRECTOR environment variable

## Executive Producer
- All permissions a Casting Director has and…
- Add or delete a movie from the database
A sample token for this role is stored in the AUTH_EXEC_PRODUCER environment variable

A token needs to be passed to each endpoint. 
The following token works for all endpoints.
Copy and paste the following into a shell:
The curl examples below will all work using the token stored in AUTH_EXEC_PRODUCER
Type the following to set this up:
```
export AUTH_TOKEN=$AUTH_EXEC_PRODUCER
```

Reset the test database with the following:
```
dropdb test_casting
createdb test_casting
python3 manage.py db upgrade
python3 add_test_data.py
```

Then copy and paste the follow curl requests

#### GET '/actors'
Returns a paginated list of all available actors, total number of actors, and a success value.
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_TOKEN" http://localhost:5000/actors 
Sample response output:
{"actors":[
        {
          "age":64,
          "gender":"m",
          "id":1,
          "name":"Tom Hanks"
        }, 
          ...
        {
          "age":48,
          "gender":"m",
          "id":5,
          "name":"Idris Elba"
        }],
        "success":true,
        "total_actors":5
        }


#### POST '/actors'
Returns a list of all actors, along with the newly created actor id, a success value, and total number of actors.
Sample curl: 
curl http://localhost:5000/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_TOKEN" -d '{"name":"Russel Crowe", "age": 56, "gender": "m"}'
Sample response output:
{"actors":[
        {
          "age":64,
          "gender":"m",
          "id":1,
          "name":"Tom Hanks"
        }, 
          ...
        {
          "age":24,
          "gender":"m",
          "id":14,
          "name":"Tom Holland"
          }],
          "created":14,
          "success":true,
          "total_actors":6
        }


#### DELETE '/actors/{actor_id}'
Returns a list of all actors after deleting the requested actor, the deleted actor id, a success value, and total number of actors.
curl http://localhost:5000/actors/6 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_TOKEN" 
{"actors":[
        {
          "age":64,
          "gender":"m",
          "id":1,
          "name":"Tom Hanks"
        },
          ...
        {
          "age":48,
          "gender":"m",
          "id":5,
          "name":"Idris Elba"
          }
        ],
        "deleted":14,
        "success":true,
        "total_actors":5
}

 
#### GET '/movies'
Returns a list of all movies, any actors cast in a movie, total number of movies, and a success value.
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_TOKEN" http://localhost:5000/movies
Sample response output:
{"movies":[
        {
          "actors":[
                  {
                    "age":45,
                    "gender":"f",
                    "id":2,
                    "name":"Charlize Theron"
                  },
                  {
                    "age":41,
                    "gender":"f",
                    "id":4,"name":
                    "Noomi Rapace"
                  }
                ],
          "id":1,
          "releasedate":"Fri, 08 Jun 2012 00:00:00 GMT",
          "title":"Prometheus"
        },
        {
          "actors":[],
          "id":2,
          "releasedate":"Fri, 25 Jun 1982 00:00:00 GMT",
          "title":"Blade Runner"
        },
        {
          "actors":[],
          "id":3,
          "releasedate":"Fri, 24 May 1991 00:00:00 GMT",
          "title":"Thelma and Louise"
        }
        ],
        "success":true,
        "total_movies":3}

#### POST '/movies/create'
Returns a paginated list of all movies, along with new product posted, a success value, and total number of items.
Sample curl: 
curl http://localhost:5000/movies/create -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_TOKEN" -d '{"title":"Gladiator", "releasedate": "2000-05-12"}'
Sample response output:
{"movies":[
        {
          "actors":[
                  {
                    "age":45,
                    "gender":"f",
                    "id":2,
                    "name":"Charlize Theron"
                  },
                  {
                    "age":41,
                    "gender":"f",
                    "id":4,"name":
                    "Noomi Rapace"
                  }
                ],
          "id":1,
          "releasedate":"Fri, 08 Jun 2012 00:00:00 GMT",
          "title":"Prometheus"
        },
          ...
        {
          "actors":[],
          "id":4,
          "releasedate":"Fri, 05 May 2000 00:00:00 GMT",
          "title":"Gladiator"
        }
   ],
   "success":true,
   "total_movies":4}
        

#### DELETE '/movies/{movie_id}'
Returns a list of all items after deleting the requested item, a success value, and total number of items.
curl http://localhost:5000/movies/4 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_TOKEN" 
{"movies":[
        {
          "actors":[
                  {
                    "age":45,
                    "gender":"f",
                    "id":2,
                    "name":"Charlize Theron"
                  },
                  {
                    "age":41,
                    "gender":"f",
                    "id":4,"name":
                    "Noomi Rapace"
                  }
                ],
          "id":1,
          "releasedate":"Fri, 08 Jun 2012 00:00:00 GMT",
          "title":"Prometheus"
        },
          ...
        {
          "actors":[],
          "id":3,
          "releasedate":"Fri, 24 May 1991 00:00:00 GMT",
          "title":"Thelma and Louise"
        }
        ],
        "success":true,
        "total_movies":3,
        "deleted":4}

#### PATCH '/movies/cast/{movie_id}'
Returns a paginated list of all movies, along with new product posted, a success value, and total number of items.
Sample curl: 
curl http://localhost:5000/movies/cast/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_TOKEN" -d '{"id":5}'
Sample response output:
{"production":{
        "actors":[
                {
                        "age":45,
                        "gender":"f",
                        "id":2,
                        "name":"Charlize Theron"
                },
                {
                        "age":41,
                        "gender":"f",
                        "id":4,
                        "name":"Noomi Rapace"
                },
                {
                        "age":48,
                        "gender":"m",
                        "id":5,
                        "name":"Idris Elba"
                }
        ],
        "id":1,
        "releasedate":"Fri, 08 Jun 2012 00:00:00 GMT",
        "title":"Prometheus"},
        "success":true}

## Testing
There are 19 unittests in test_app.py. To run this file use:
```
dropdb test_casting
createdb test_casting
python test_app.py
```
The tests include one test for expected success and error behavior for each endpoint, and tests demonstrating role-based access control, 
where all endpoints are tested with the correct authorization.


## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
The JWT token contains the permissions for the 'user' and 'seller' roles.

## DEPLOYMENT
The app is hosted live on heroku at the URL: 
https://warranty-tracker.herokuapp.com

However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with curl or postman.