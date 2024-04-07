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
from models import db, User, People
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

# -----------------PEOPLE--------------------
@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    result = list(map(lambda person: person.serialize(), all_people))

    return jsonify(result), 200

@app.route('/people/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = People.query.filter_by(id=person_id).first()

    return jsonify(person.serialize())

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

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
