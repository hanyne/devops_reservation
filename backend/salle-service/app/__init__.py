from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Nothing123@db:5432/reservation_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuration JWT
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Modifie cela pour ta clé secrète
    
    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Enregistrement du Blueprint
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # Affichage des routes pour débogage
    with app.app_context():
        print("\nRegistered routes:")
        for rule in app.url_map.iter_rules():
            print(rule)

    return app
