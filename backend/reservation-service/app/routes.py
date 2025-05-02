from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import Reservation, User, Salle
from . import db
from .kafka_handler import get_kafka_producer
import datetime

reservation_bp = Blueprint('reservation_bp', __name__)

# Route pour l'authentification (génération de token JWT)
@reservation_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Authentification simple (à remplacer par une vraie vérification en production)
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity={'username': username, 'role': 'admin'})
        return jsonify({'access_token': access_token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# Route pour obtenir toutes les réservations
@reservation_bp.route('/reservations', methods=['GET'])
@jwt_required()
def get_reservations():
    reservations = Reservation.query.all()
    return jsonify([r.to_dict() for r in reservations]), 200

# Route pour créer une réservation
@reservation_bp.route('/reservations', methods=['POST'])
@jwt_required()
def create_reservation():
    data = request.get_json()
    user_id = data.get('user_id')
    salle_id = data.get('salle_id')
    start_time = datetime.datetime.fromisoformat(data.get('start_time'))
    end_time = datetime.datetime.fromisoformat(data.get('end_time'))

    # Vérifier si l'utilisateur et la salle existent
    user = User.query.get(user_id)
    salle = Salle.query.get(salle_id)
    if not user or not salle:
        return jsonify({'error': 'User or salle not found'}), 404

    # Vérifier les conflits de réservation
    conflict = Reservation.query.filter(
        Reservation.salle_id == salle_id,
        Reservation.start_time < end_time,
        Reservation.end_time > start_time
    ).first()
    if conflict:
        return jsonify({'error': 'Salle already reserved for this time slot'}), 409

    # Créer la réservation
    reservation = Reservation(
        user_id=user_id,
        salle_id=salle_id,
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(reservation)
    db.session.commit()

    # Publier un événement Kafka
    try:
        producer = get_kafka_producer()
        event = {
            'reservation_id': reservation.id,
            'user_id': user_id,
            'salle_id': salle_id,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'status': 'created'
        }
        producer.send('reservations_topic', event)
        producer.flush()
        print(f"Published event to Kafka: {event}")
    except Exception as e:
        print(f"Failed to publish to Kafka: {e}")

    return jsonify({'message': 'Réservation créée', 'id': reservation.id}), 201