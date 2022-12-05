from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# PEOPLE

class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            }

# PLANETS

class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    gravity = db.Column(db.String(120), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            }


# FAVS

peopleFavs = db.Table("peopleFav",
     db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
     db.Column("people_id", db.Integer, db.ForeignKey("people.id"), primary_key=True)
)

planetsFavs = db.Table("planetsFav",
     db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
     db.Column("planets_id", db.Integer, db.ForeignKey("planets.id"), primary_key=True)
)

# USERS

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    peopleFav = db.relationship(People,
                    secondary=peopleFavs,
                    lazy='subquery',
                    backref=db.backref('users', lazy=True))
    planetsFav = db.relationship(Planets,
                    secondary=planetsFavs,
                    lazy='subquery',
                    backref=db.backref('users', lazy=True))



    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            # Return favs:
            "peopleFav": self.obtain_peopleFav(),
            "planetsFav": self.obtain_planetsFav(),         
        }
    
    def obtain_peopleFav(self):
        return list(map(lambda x: x.serialize(), self.peopleFav))

    def obtain_planetsFav(self):
        return list(map(lambda x: x.serialize(), self.planetsFav))