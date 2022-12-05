"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets
import requests


# Requests

r = requests.get('https://google.com')
print("RESULT", r)

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints

@app.route('/')
def sitemap():
    return generate_sitemap(app)



# ------------------- USERS -------------------->>

# GET or POST users

@app.route('/user', methods=['POST','GET'])
def handle_user():

    if request.method == 'POST':
        body = request.get_json()
        user = User(
            email= body['email'],
            password=body['password'],
            is_active=True         
        )
        db.session.add(user)
        db.session.commit()
        response_body = {
        "msg": "User added correctly!"
        }
        return jsonify(response_body), 200

    if request.method == 'GET':
        all_user = User.query.all()
        all_user =list(map(lambda x: x.serialize(), all_user))
        response_body = all_user
        return jsonify(response_body), 200



# ------------------- FAVORITES -------------------->>

# User FAVORITES

@app.route('/user/<int:id_user>/favorites', methods=['GET'])
def obtener_favoritos(id_user):

    response_people = User.query.filter_by(id=id_user).first().peopleFav
    response_planets = User.query.filter_by(id=id_user).first().planetsFav
    People = list(map(lambda x: x.serialize(), response_people))
    Planets = list(map(lambda x: x.serialize(), response_planets))

    return jsonify({
        "PeopleFav": People,
        "PlanetsFav": Planets
    }), 200


# Add FAVORITE character to a specific USER ID

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_fav(people_id):
    id_user = 2
    user = User.query.get(id_user)
    character = People.query.get(people_id)
    print(id_user)
    favList = User.query.filter_by(id=id_user).first().peopleFav
    favList.append(character)
    db.session.commit()

    return jsonify({
        "msg": "Your favorite character has been added correctly :)",
        "PeopleFav": list(map(lambda x: x.serialize(), favList))
    }), 200


# Select a USER ID and a FAVORITE character to add to FAVORITES

@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def handle_people_favorites(user_id, people_id):
    id_user = user_id
    user = User.query.get(id_user)
    character = People.query.get(people_id)
    print(id_user)
    favList = User.query.filter_by(id=id_user).first().peopleFav
    favList.append(character)
    db.session.commit()

    return jsonify({
        "msg": "Your favorite character has been added correctly :)",
        "PeopleFav": list(map(lambda x: x.serialize(), favList))
    }), 200


# Delete FAVORITE character from a specific USER ID

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_character_fav(people_id):
    id_user = 2
    user = User.query.get(id_user)
    character = People.query.get(people_id)
    favList = User.query.filter_by(id=id_user).first().peopleFav
    favList.remove(character)
    db.session.commit()

    return jsonify({
        "success": "Your favorite character has been deleted correctly :(",
        "PlanetsFav": list(map(lambda x: x.serialize(), favList))
    }), 200


# Add FAVORITE planet to a specific USER ID

@app.route('/favorite/planets/<int:planets_id>', methods=['POST'])
def add_planet_fav(planets_id):
    id_user = 2  
    user = User.query.get(id_user)
    planet = Planets.query.get(planets_id)
    favList = User.query.filter_by(id=id_user).first().planetsFav
    favList.append(planet)
    db.session.commit()

    return jsonify({
        "msg": "Your favorite planet has been added correctly :)",
        "PlanetsFav": list(map(lambda x: x.serialize(), favList))
    }), 200


# Select a USER ID and a FAVORITE character to add to FAVORITES

@app.route('/user/<int:user_id>/favorite/planets/<int:planets_id>', methods=['POST'])
def handle_planet_favorites(user_id, planets_id):
    id_user = user_id
    user = User.query.get(id_user)
    planet = Planets.query.get(planets_id)
    favList = User.query.filter_by(id=id_user).first().planetsFav
    favList.append(planet)
    db.session.commit()

    return jsonify({
        "msg": "Your favorite planet has been added correctly :)",
        "PlanetsFav": list(map(lambda x: x.serialize(), favList))
    }), 200


# Delete FAVORITE planet from a specific USER ID

@app.route('/favorite/planets/<int:planets_id>', methods=['DELETE'])
def remove_planet_fav(planets_id):
    id_user = 2
    user = User.query.get(id_user)
    planet = Planets.query.get(planets_id)
    favList = User.query.filter_by(id=id_user).first().planetsFav
    favList.remove(planet)
    db.session.commit()
    return jsonify({
        "msg": "Your favorite planet has been deleted correctly :(",
        "PlanetsFav": list(map(lambda x: x.serialize(), favList))
    }), 200



# ------------------- PEOPLE -------------------->>

# GET or POST characters

@app.route('/people', methods=['GET', 'POST'])
def handle_people():

    if request.method == 'POST':
        body = request.get_json()
        character = People(
            name=body['name'], 
            height= body['height'],
            mass=body['mass']
        )
        db.session.add(character)
        db.session.commit()
        response_body = {
        "msg": "Character added correctly!"
        }
        return jsonify(response_body), 200

    if request.method == 'GET':
        all_people = People.query.all()
        all_people =list(map(lambda x: x.serialize(), all_people))
        response_body = all_people
        return jsonify(response_body), 200


# DELETE character based on its ID

@app.route('/people/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character_delete = People.query.get(character_id)
    if not character_delete:
        response_body = {
            "msg" : "This character does not exist, can't be deleted."
        }
        return jsonify(response_body), 200
        
    db.session.delete(character_delete)
    db.session.commit()
    response_body = {
        "msg" : "Character deleted correctly."
    }

    return jsonify(response_body), 200


# GET a character based on its ID

@app.route('/people/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character_query = People.query.get(character_id)
    
    if not character_query:
        response_body = {
            "msg" : "The character you are looking for does not exist."
        }
        return jsonify(response_body), 200

    data_character = character_query.serialize()
    return jsonify({
        "result": data_character
    }), 200



# ------------------- PLANETS -------------------->>

# GET or POST planets

@app.route('/planets', methods=['GET', 'POST'])
def handle_planets():

    if request.method == 'POST':
        body = request.get_json()
        planet = Planets(
            name=body['name'],
            diameter = body['diameter'], 
            gravity = body['gravity'],
            population = body['population']
        )
        db.session.add(planet)
        db.session.commit()
        response_body = {
        "msg": "Planet added correctly!"
        }
        return jsonify(response_body), 200

    if request.method == 'GET':
        all_planets = Planets.query.all()
        all_planets =list(map(lambda x: x.serialize(), all_planets))
        response_body = all_planets
        return jsonify(response_body), 200


# DELETE planet based on its ID

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet_delete = Planets.query.get(planet_id)
    if not planet_delete:
        response_body = {
            "msg" : "This planet does not exist, can't be deleted."
        }
        return jsonify(response_body), 200

    db.session.delete(planet_delete)
    db.session.commit()
    response_body = {
        "msg" : "Planet deleted correctly."
    }

    return jsonify(response_body), 200


# GET a planet based on its ID

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet_query = Planets.query.get(planet_id)
    
    if not planet_query:
        response_body = {
            "msg" : "The planet you are looking for does not exist."
        }
        return jsonify(response_body), 200

    data_planet = planet_query.serialize()
    return jsonify({
        "result": data_planet
    }), 200







# ------------------- LAST LINES -------------------->>

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


