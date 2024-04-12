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
from models import db, User, People, Planet, Starship, FavoritePlanet, FavoritePeople, FavoriteStarship
from sqlalchemy import and_
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
#-----------------USERS---------------------
@app.route('/user', methods=['GET'])
def get_all_user():
    all_user = User.query.all()
    result = list(map(lambda user : user.serialize(),all_user))

    return jsonify(result), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):    
    user = User.query.filter_by(id=user_id).first()
    
    return jsonify(user.serialize()), 200

@app.route('/user', methods=['POST'])
def add_user():
    body = request.get_json()
    user = User(
        email = body['email'], 
        password = body['password'], 
        is_active = True)
    db.session.add(user)
    db.session.commit()

    response_body = {
        "msg" : "user added succesfully"
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()

    response_body = {
        "msg" : "user deleted sucesfully"
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    body = request.get_json()

    user.email = body['email']
    user.password = body['password']

    db.session.commit()

    response_body = {
        "msg" : "user updated succesfully"
    }
    return jsonify(response_body), 200

# -----------------PEOPLE--------------------
@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    result = list(map(lambda person: person.serialize(), all_people))

    return jsonify(result), 200

@app.route('/people/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = People.query.filter_by(id=person_id).first()

    return jsonify(person.serialize()),200

@app.route('/people', methods=['POST'])
def add_person():
    body = request.get_json()
    person = People(
        name = body['name'],
        height = body['height'],
        hair_color = body['hair_color'],
        gender = body['gender']
    )
    db.session.add(person)
    db.session.commit()

    response_body = {
        "msg" : "person added succesfully"
    }
    return jsonify(response_body), 200

@app.route('/people/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):    
    person = People.query.filter_by(id=person_id).first()
    db.session.delete(person)
    db.session.commit()

    response_body = {
        "msg" : "person deleted succesfully"
    }
    return jsonify(response_body), 200

@app.route('/people/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    person = People.query.filter_by(id=person_id).first()
    body = request.get_json()

    person.gender = body['gender'],
    person.hair_color = body['hair_color'],
    person.height = body['height'],
    person.name = body['name']   
    
    db.session.commit()

    response_body = {
        "msg" : "person updated succesfully"
    }
    return jsonify(response_body), 200

#-------------------PLANETS---------------------
@app.route('/planet', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    result = list(map(lambda planet: planet.serialize() , all_planets))

    return jsonify(result), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()

    return jsonify(planet.serialize()),200

@app.route('/planet', methods=['POST'])
def add_planet():
    body = request.get_json()
    planet = Planet(
        climate = body['climate'],
        name = body['name'],
        rotation_period = body['rotation_period'],
        terrain = body['terrain']
    )

    db.session.add(planet)
    db.session.commit()

    response_body = {
        "msg" : "planet added succesfully"
    }

    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    db.session.delete(planet)
    db.session.commit()

    response_body = {
        "msg" : "planet deleted succesfully"
    }
    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    body = request.get_json()
    
    planet.climate = body['climate'],
    planet.name = body['name'],
    planet.rotation_period = body['rotation_period'],
    planet.terrain = body['terrain']

    db.session.commit()

    response_body = {
        "msg" : "planet updated succesfully"
    }
    return jsonify(response_body), 200

#-------------------STARSHIPS--------------------

@app.route('/starship', methods=['GET'])
def get_starships():
    all_starships = Starship.query.all()
    result = list(map(lambda starship : starship.serialize(), all_starships))

    return jsonify(result), 200

@app.route('/starship/<int:starship_id>', methods=['GET'])
def get_starship(starship_id):
    starship = Starship.query.filter_by(id=starship_id).first()
    
    return jsonify(starship.serialize())

@app.route('/starship', methods=['POST'])
def add_starship():
    body = request.get_json()
    starship = Starship(
        cost_in_credits = body['cost_in_credits'],
        crew = body['crew'],
        model = body['model'],
        name = body['name']
    )
    db.session.add(starship)
    db.session.commit()

    response_body = {
        "msg" : "starship added succesfully"
    }
    return jsonify(response_body), 200

@app.route('/starship/<int:starship_id>', methods=['DELETE'])
def delete_starship(starship_id):
    starship = Starship.query.filter_by(id=starship_id).first()
    db.session.delete(starship)
    db.session.commit()

    response_body = {
        "msg" : "starship deleted sucesfully"
    }
    return jsonify(response_body), 200

@app.route('/starship/<int:starship_id>', methods=['PUT'])
def update_starship(starship_id):
    starship = Starship.query.filter_by(id=starship_id).first()
    body = request.get_json()
    
    starship.cost_in_credits = body['cost_in_credits'],
    starship.crew = body['crew'],
    starship.model = body['model'],
    starship.name = body['name']

    db.session.commit() 

    response_body = {
        "msg" : "starship updated sucesfully"
    }
    return jsonify(response_body), 200

#-----------------Favorites-----------------
@app.route('/user/<int:user_id>/favorites/people', methods=['GET'])
def get_favorite_people(user_id):
    favorites = FavoritePeople.query.filter_by(user_id=user_id).all()
    result = list(map(lambda favorite : favorite.serialize(), favorites))
    
    return jsonify(result)

@app.route('/user/<int:user_id>/favorites/people/<int:people_id>', methods=['POST'])
def create_favorite_people(user_id, people_id):
    
    new_favorite = FavoritePeople(
        user_id = user_id,
        people_id = people_id
    )
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "msg" : "favorite added succesfully"
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    favorite_to_delete = FavoritePeople.query.filter_by(user_id=user_id, people_id=people_id).first()
    
    db.session.delete(favorite_to_delete)
    db.session.commit()

    response_body = {
        "msg" : "favorite deleted succesfully"
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites/planet', methods=['GET'])
def get_favorite_planet(user_id):

    favorites = FavoritePlanet.query.filter_by(user_id=user_id).all()
    result = list(map(lambda favorite: favorite.serialize() ,favorites))

    return jsonify(result), 200

@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['POST'])
def create_favorite_planet(user_id, planet_id):

    new_favorite = FavoritePlanet(
        user_id = user_id,
        planet_id = planet_id
    )
    db.session.add(new_favorite)
    db.session.commit()
    
    response_body = {
        "msg": "favorite added succesfully"
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorite_to_delete = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()

    db.session.delete(favorite_to_delete)
    db.session.commit()

    response_body = {
        "msg": "favorite deleted succesfully"
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites/starship', methods=['GET'])
def get_favorite_starship(user_id):
    favorites = FavoriteStarship.query.filter_by(user_id=user_id).all()
    result = list(map(lambda favorite: favorite.serialize(), favorites))

    return jsonify(result), 200

@app.route('/user/<int:user_id>/favorites/starship/<int:starship_id>', methods=['POST'])
def create_favorite_starship(user_id, starship_id):

    new_favorite = FavoriteStarship(
        user_id = user_id,
        starship_id = starship_id
    )
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "msg": "favorite created succesfully"
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites/starship/<int:starship_id>', methods=['DELETE'])
def delete_favorite_starship(user_id, starship_id):
    favorite_to_delete = FavoriteStarship.query.filter_by(user_id=user_id, starship_id=starship_id).first()
    
    db.session.delete(favorite_to_delete)
    db.session.commit()

    response_body = {
        "msg": "favorite created succesfully"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
