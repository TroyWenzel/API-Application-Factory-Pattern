from app.blueprints.parts import parts_bp
from flask import jsonify, request
from marshmallow import ValidationError
from app.models import db, Inventory, Parts
from app.blueprints.parts.schemas import inventory_schema, inventories_schema, part_schema, parts_schema
from app.extensions import limiter
from app.util.auth import token_required

# ============== INVENTORY ROUTES ==============

# CREATE INVENTORY ITEM
@parts_bp.route('/inventory', methods=['POST'])
@token_required
def create_inventory():
    try:
        new_inventory = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201

# READ ALL INVENTORY
@parts_bp.route('/inventory', methods=['GET'])
def read_inventory():
    inventory_items = db.session.query(Inventory).all()
    return inventories_schema.jsonify(inventory_items), 200

# READ SINGLE INVENTORY ITEM
@parts_bp.route('/inventory/<int:inventory_id>', methods=['GET'])
def read_inventory_item(inventory_id):
    inventory_item = db.session.get(Inventory, inventory_id)
    
    if not inventory_item:
        return jsonify({'error': 'Inventory item not found'}), 404
    
    return inventory_schema.jsonify(inventory_item), 200

# UPDATE INVENTORY ITEM
@parts_bp.route('/inventory/<int:inventory_id>', methods=['PUT'])
@token_required
def update_inventory(inventory_id):
    inventory_item = db.session.get(Inventory, inventory_id)
    
    if not inventory_item:
        return jsonify({'error': 'Inventory item not found'}), 404
    
    try:
        data = request.json
        for key, value in data.items():
            if hasattr(inventory_item, key):
                setattr(inventory_item, key, value)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    db.session.commit()
    return inventory_schema.jsonify(inventory_item), 200

# DELETE INVENTORY ITEM
@parts_bp.route('/inventory/<int:inventory_id>', methods=['DELETE'])
@limiter.limit("5 per day")
@token_required
def delete_inventory(inventory_id):
    inventory_item = db.session.get(Inventory, inventory_id)
    
    if not inventory_item:
        return jsonify({'error': 'Inventory item not found'}), 404
    
    db.session.delete(inventory_item)
    db.session.commit()
    return jsonify({'message': f'Inventory item {inventory_id} deleted'}), 200


# ============== PARTS ROUTES ==============

# CREATE PART
@parts_bp.route('', methods=['POST'])
@token_required
def create_part():
    try:
        new_part = part_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    db.session.add(new_part)
    db.session.commit()
    return part_schema.jsonify(new_part), 201

# READ ALL PARTS
@parts_bp.route('', methods=['GET'])
def read_parts():
    parts = db.session.query(Parts).all()
    return parts_schema.jsonify(parts), 200

# READ SINGLE PART
@parts_bp.route('/<int:part_id>', methods=['GET'])
def read_part(part_id):
    part = db.session.get(Parts, part_id)
    
    if not part:
        return jsonify({'error': 'Part not found'}), 404
    
    return part_schema.jsonify(part), 200

# UPDATE PART
@parts_bp.route('/<int:part_id>', methods=['PUT'])
@token_required
def update_part(part_id):
    part = db.session.get(Parts, part_id)
    
    if not part:
        return jsonify({'error': 'Part not found'}), 404
    
    try:
        data = request.json
        for key, value in data.items():
            if hasattr(part, key):
                setattr(part, key, value)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    db.session.commit()
    return part_schema.jsonify(part), 200

# DELETE PART
@parts_bp.route('/<int:part_id>', methods=['DELETE'])
@token_required
def delete_part(part_id):
    part = db.session.get(Parts, part_id)
    
    if not part:
        return jsonify({'error': 'Part not found'}), 404
    
    db.session.delete(part)
    db.session.commit()
    return jsonify({'message': f'Part {part_id} deleted'}), 200

# GET AVAILABLE PARTS (parts not assigned to any ticket)
@parts_bp.route('/available', methods=['GET'])
def get_available_parts():
    available_parts = db.session.query(Parts).filter(Parts.ticket_id == None).all()
    return parts_schema.jsonify(available_parts), 200