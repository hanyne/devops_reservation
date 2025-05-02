from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from .models import Salle
from . import db
from .utils import check_availability, update_availability

bp = Blueprint('routes', __name__)

# Route pour la connexion (authentification)
@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Vérification des identifiants (à remplacer par une vraie vérification)
    if username == "admin" and password == "password":
        access_token = create_access_token(identity={"username": username, "role": "Admin"})
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Route pour récupérer les salles
@bp.route('/salles', methods=['GET'])
@jwt_required()
def get_salles():
    salles = Salle.query.all()
    return jsonify([{"id": salle.id, "name": salle.name, "capacity": salle.capacity, "available": salle.available} for salle in salles])

# Route pour créer une salle
@bp.route('/salles', methods=['POST'])
@jwt_required()
def create_salle():
    current_user = get_jwt_identity()
    if current_user['role'] not in ["Admin", "Employé"]:
        return jsonify({"message": "Accès non autorisé"}), 403
    
    data = request.get_json()
    salle = Salle(name=data['name'], capacity=data['capacity'])
    db.session.add(salle)
    db.session.commit()
    return jsonify({"message": "Salle créée", "name": salle.name}), 201

# Route pour vérifier la disponibilité d'une salle
@bp.route('/salles/<int:salle_id>/availability', methods=['GET'])
@jwt_required()
def get_availability(salle_id):
    available = check_availability(salle_id)
    return jsonify({"salle_id": salle_id, "available": available})

# Route pour mettre à jour la disponibilité d'une salle
@bp.route('/salles/<int:salle_id>/availability', methods=['PUT'])
@jwt_required()
def set_availability(salle_id):
    data = request.get_json()
    update_availability(salle_id, data['available'])
    return jsonify({"message": "Disponibilité mise à jour"})
