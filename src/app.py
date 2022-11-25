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
from models import db, User, People, Planet
#from models import Person

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

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['POST','GET'])
def handle_user():

    if request.method == 'POST':
        body = request.get_json()
        user = User(
            name=body['name'], 
            email= body['email'],
            password=body['password'],
            
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


@app.route('/planets', methods=['GET', 'POST'])
def handle_planets():

    if request.method == 'POST':
        body = request.get_json()
        planet = Planet(
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
        all_planets = Planet.query.all()
        all_planets =list(map(lambda x: x.serialize(), all_planets))
        response_body = all_planets
        return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
