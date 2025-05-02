from .models import Salle
from . import db

def check_availability(salle_id):
    salle = Salle.query.get(salle_id)
    if salle:
        return salle.available
    return False

def update_availability(salle_id, available):
    salle = Salle.query.get(salle_id)
    if salle:
        salle.available = available
        db.session.commit()
