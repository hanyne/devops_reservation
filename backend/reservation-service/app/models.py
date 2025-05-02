from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Salle(db.Model):
    __tablename__ = 'salles'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    capacite = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "capacite": self.capacite
        }

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    salle_id = db.Column(db.Integer, db.ForeignKey('salles.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref='reservations')
    salle = db.relationship('Salle', backref='reservations')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "salle_id": self.salle_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "user": self.user.to_dict(),
            "salle": self.salle.to_dict()
        }