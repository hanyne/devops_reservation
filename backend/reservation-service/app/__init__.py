from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialisation des extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Nothing123@db:5432/reservation_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # À remplacer par une clé sécurisée en production

    # Initialisation des extensions
    db.init_app(app)
    jwt.init_app(app)

    # Import et enregistrement des routes
    from .routes import reservation_bp
    app.register_blueprint(reservation_bp)

    print("Blueprint 'reservation_bp' registered successfully")

    return app