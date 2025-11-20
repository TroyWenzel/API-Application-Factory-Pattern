from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, customers_schema
from flask import jsonify, request
from marshmallow import ValidationError
from app.models import db, Customers
from app.extensions import limiter

# CREATE CUSTOMER ROUTE
@customers_bp.route('', methods=['POST'])
@limiter.limit("2 per day")
def create_customer():
    try:
        new_customer = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# READ CUSTOMERS ROUTE
@customers_bp.route("", methods=["GET"])
def read_customers():
    customers = db.session.query(Customers).all()
    return customers_schema.jsonify(customers), 200

# Read Individual Customer
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def read_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return customer_schema.jsonify(customer), 200

# Delete a Customer
@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
@limiter.limit("5 per day")
def delete_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted customer {customer_id}"}), 200

# UPDATE A CUSTOMER
@customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    try:
        updated_customer = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for attr in ["first_name", "last_name", "email", "phone"]: 
        if hasattr(updated_customer, attr):
            setattr(customer, attr, getattr(updated_customer, attr))
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200

# SEARCH CUSTOMER BY EMAIL (case-insensitive)
@customers_bp.route('/search', methods=['GET'])
def search_customer_by_email():
    email = request.args.get('email')
    
    if not email:
        return jsonify({'error': 'Email parameter is required'}), 400
    
    # Case-insensitive search
    customer = db.session.query(Customers).filter(Customers.email.ilike(email)).first()
    
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    return customer_schema.jsonify(customer), 200