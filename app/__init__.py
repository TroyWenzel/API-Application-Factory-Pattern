from flask import Flask, jsonify
from app.models import db
from app.extensions import ma, limiter, cache
from app.blueprints.user import users_bp
from app.blueprints.books import books_bp
from app.blueprints.loans import loans_bp
from app.blueprints.orders import orders_bp
from app.blueprints.items import items_bp
from flask_swagger_ui import get_swaggerui_blueprint
from merge_swagger import merged_swagger  # Import the merged swagger

SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'  # Changed from static YAML to dynamic JSON

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    # Serve merged swagger as JSON endpoint
    @app.route('/api/swagger.json')
    def swagger_json():
        if merged_swagger:
            return jsonify(merged_swagger)
        else:
            return jsonify({"error": "Swagger documentation not available"}), 500
    
    # Register blueprints
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(loans_bp, url_prefix='/loans')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(items_bp, url_prefix='/items')
    
    # Register Swagger UI blueprint
    swagger_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, 
        API_URL, 
        config={'app_name': 'Mechanic Shop API'}
    )
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
    
    return app
