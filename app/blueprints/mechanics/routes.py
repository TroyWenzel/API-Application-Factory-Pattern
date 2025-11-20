from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema, login_schema
from app.models import db, Mechanics, ServiceTickets
from app.extensions import limiter
from app.blueprints.service_tickets.schemas import service_tickets_schema
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.auth import encode_token, token_required

# LOGIN ROUTE
@mechanics_bp.route('/login', methods=['POST'])
@limiter.limit("5 per 10 minute")
def login():
    try:
        data = request.json
        login_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Find mechanic by email
    mechanic = db.session.query(Mechanics).filter_by(email=data['email']).first()
    
    # Verify mechanic exists and password is correct
    if mechanic and check_password_hash(mechanic.password, str(data['password'])):
        token = encode_token(mechanic.id)
        return jsonify({"message": f"Welcome back, {mechanic.first_name}!","token": token}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401


# CREATE MECHANIC ROUTE
@mechanics_bp.route('', methods=['POST'])
#@limiter.limit("2 per day")
def create_mechanic():
    try:
        data = request.json
    except ValidationError as e:
        return jsonify(e.messages), 400

        
    data["password"] = generate_password_hash(str(data["password"]))

    mechanic = Mechanics(**data)
    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201


# READ ALL MECHANICS
@mechanics_bp.route('', methods=['GET'])
def read_mechanics():
    mechanics = db.session.query(Mechanics).all()
    return mechanics_schema.jsonify(mechanics), 200


# GET MY TICKETS - Requires Token
@mechanics_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets():
    mechanic_id = request.logged_in_mechanic_id
    # Get the mechanic and their tickets through the relationship
    mechanic = db.session.get(Mechanics, mechanic_id)   
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404 
    # Return tickets (you'll need to import service_tickets_schema)
    return service_tickets_schema.jsonify(mechanic.service_tickets), 200


# GET MY PROFILE - Requires Token
@mechanics_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    mechanic_id = request.logged_in_mechanic_id
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404
    
    return mechanic_schema.jsonify(mechanic), 200


# UPDATE MECHANIC - Requires Token
@mechanics_bp.route('', methods=['PUT'])
@limiter.limit("5 per day")
@token_required
def update_mechanic():
    mechanic_id = request.logged_in_mechanic_id
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404

    try:
        data = request.json
        if 'password' in data:
            data['password'] = generate_password_hash(data['password'])
        
        for key, value in data.items():
            if hasattr(mechanic, key):
                setattr(mechanic, key, value)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


# DELETE MECHANIC - Requires Token
@mechanics_bp.route('', methods=['DELETE'])
@token_required
def delete_mechanic():
    mechanic_id = request.logged_in_mechanic_id
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message': 'Mechanic deleted'}), 200

# GET MECHANIC WITH MOST TICKETS
@mechanics_bp.route('/top-mechanics', methods=['GET'])
def get_top_mechanics():
    from sqlalchemy import func
    from app.models import ticket_mechanic
    
    # Query to count tickets per mechanic
    results = db.session.query(
        Mechanics.id,
        Mechanics.first_name,
        Mechanics.last_name,
        Mechanics.email,
        func.count(ticket_mechanic.c.ticket_id).label('ticket_count')
    ).join(
        ticket_mechanic, Mechanics.id == ticket_mechanic.c.mechanic_id
    ).group_by(
        Mechanics.id
    ).order_by(
        func.count(ticket_mechanic.c.ticket_id).desc()
    ).limit(5).all()
    if not results:
        return jsonify({'error': 'No mechanics found with tickets'}), 404
    
    top_mechanics = [
        {
            'id': result.id,
            'first_name': result.first_name,
            'last_name': result.last_name,
            'email': result.email,
            'ticket_count': result.ticket_count
        }
        for result in results
    ]
    
    return jsonify(top_mechanics), 200