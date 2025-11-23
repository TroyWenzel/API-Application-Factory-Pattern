from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, customers_schema, customer_login_schema
from flask import jsonify, request
from marshmallow import ValidationError
from app.models import db, Customers, ServiceTickets
from app.extensions import limiter, cache
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.auth import encode_token, customer_token_required

# CUSTOMER LOGIN ROUTE
@customers_bp.route('/login', methods=['POST'])
@limiter.limit("5 per 10 minute")
def login():
    try:
        data = request.json
        customer_login_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Find customer by email
    customer = db.session.query(Customers).filter_by(email=data['email']).first()
    
    # Verify customer exists and password is correct
    if customer and check_password_hash(customer.password, str(data['password'])):
        token = encode_token(customer.id, role="customer")
        return jsonify({
            "message": f"Welcome back, {customer.first_name}!",
            "token": token
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401


# CREATE CUSTOMER ROUTE
@customers_bp.route('', methods=['POST'])
@limiter.limit("2 per day")
def create_customer():
    try:
        data = request.json
        new_customer = customer_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Hash the password before saving
    if 'password' in data:
        new_customer.password = generate_password_hash(str(data['password']))
    
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


# GET MY TICKETS - Customer Token Required
@customers_bp.route('/my-tickets', methods=['GET'])
@customer_token_required
def get_my_tickets():
    customer_id = request.logged_in_customer_id
    
    # Get all service tickets for this customer
    tickets = db.session.query(ServiceTickets).filter_by(customer_id=customer_id).all()
    
    if not tickets:
        return jsonify({"message": "No service tickets found"}), 200
    
    # Import schema for service tickets
    from app.blueprints.service_tickets.schemas import service_tickets_schema
    return service_tickets_schema.jsonify(tickets), 200


# GET MY PROFILE - Customer Token Required
@customers_bp.route('/profile', methods=['GET'])
@customer_token_required
def get_profile():
    customer_id = request.logged_in_customer_id
    customer = db.session.get(Customers, customer_id)
    
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    return customer_schema.jsonify(customer), 200


# READ CUSTOMERS ROUTE - PAGINATED WITH CACHING
@customers_bp.route("", methods=["GET"])
@cache.cached(timeout=60, query_string=True)
def read_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = db.session.query(Customers)
    paginated_customers = db.paginate(query, page=page, per_page=per_page)
    return customers_schema.jsonify(paginated_customers), 200


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


# UPDATE A CUSTOMER - Token Required (own profile only)
@customers_bp.route("", methods=["PUT"])
@customer_token_required
def update_customer():
    customer_id = request.logged_in_customer_id
    customer = db.session.get(Customers, customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    try:
        data = request.json
        
        # Hash password if it's being updated
        if 'password' in data:
            data['password'] = generate_password_hash(str(data['password']))
        
        # Update allowed fields
        for key, value in data.items():
            if hasattr(customer, key):
                setattr(customer, key, value)
                
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
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