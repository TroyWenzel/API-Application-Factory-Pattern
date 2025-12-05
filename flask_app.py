from app.models import db
from app import create_app
import merge_swagger

# Merge swagger files before creating the app
merge_swagger.merge_swagger_files()

# Create the Flask app
app = create_app('ProductionConfig')

# Create database tables
with app.app_context():
    db.create_all()