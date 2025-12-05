from flask import Flask
from app.models import db
from app.extensions import ma, limiter, cache
from app.blueprints.customers import customers_bp
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.parts import parts_bp
from flask_swagger_ui import get_swaggerui_blueprint

# Config name mapping for convenience
CONFIG_MAP = {
    'development': 'DevelopmentConfig',
    'testing': 'TestingConfig',
    'production': 'ProductionConfig'
}
swagger_blueprint = get_swaggerui_blueprint("/api/docs", "/static/mechanic_shop_swagger.yaml", config = {"app_name":"Mechanic Shop API"})

def create_app(config_name):
    app = Flask(__name__)
    
    # Map lowercase names to actual config class names
    config_class_name = CONFIG_MAP.get(config_name, config_name)
    app.config.from_object(f'config.{config_class_name}')
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    # Register blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/tickets')
    app.register_blueprint(parts_bp, url_prefix='/parts')
    app.register_blueprint(swagger_blueprint, url_prefix='/api/docs')

    return app