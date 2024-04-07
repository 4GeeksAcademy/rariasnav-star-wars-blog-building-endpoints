from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

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