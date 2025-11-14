from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema
from app.models import db, Mechanics

mechanics_bp = Blueprint('mechanics', __name__)

@mechanics_bp.route('', methods=['POST'])
def create_mechanic():
    try:
        mechanic = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201


@mechanics_bp.route('', methods=['GET'])
def read_mechanics():
    mechanics = Mechanics.query.all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404


    try:
        updated = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400


    for attr in ['name', 'specialty']:
        if hasattr(updated, attr):
            setattr(mechanic, attr, getattr(updated, attr))


    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404


    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message': 'Mechanic deleted'}), 200