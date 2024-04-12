from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_people = db.relationship('FavoritePeople', backref='user', lazy=True)
    favorite_planet = db.relationship('FavoritePlanet', backref='user', lazy=True)
    favorite_starship = db.relationship('FavoriteStarship', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email   
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    hair_color = db.Column(db.String(250), unique=False, nullable=False)
    gender = db.Column(db.String(250), unique=False, nullable=False)
    favorite = db.relationship('FavoritePeople', backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "hair_color": self.hair_color,
            "gender": self.gender            
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(250), unique=False, nullable=False)
    terrain = db.Column(db.String(250), unique=False, nullable=False)
    favorite = db.relationship('FavoritePlanet', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "climate": self.climate,
            "terrain": self.terrain
        }
    
class Starship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    model = db.Column(db.String(250), unique=True, nullable=False)
    cost_in_credits = db.Column(db.Integer, unique=False, nullable=False)
    crew = db.Column(db.Integer, unique=False, nullable=False)
    favorite = db.relationship('FavoriteStarship', backref='starship', lazy=True)

    def __repr__(self):
        return '<Starship %r>' % self.name

    def serialize(self):
        return {
            "id" :self.id,
            "name": self.name,
            "model": self.model, 
            "cost_in_credits": self.cost_in_credits,
            "crew": self.crew
        }
    
class FavoritePeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    
    def __repr__(self):
        return '<Favorite %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id
        }
    
class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    
    def __repr__(self):
        return '<Favorite %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }
    
class FavoriteStarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'), nullable=False)
    
    def __repr__(self):
        return '<Favorite %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starship_id": self.starship_id
        }