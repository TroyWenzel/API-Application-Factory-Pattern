from app.models import db
from app import create_app
import os
import merge_swagger

# Merge swagger files before creating the app
print("=" * 60)
print("Initializing Flask Application")
print("=" * 60)

try:
    print("\n🔄 Merging Swagger files...")
    import merge_swagger
    if merge_swagger.merged_swagger:
        print("✅ Swagger merge completed successfully\n")
    else:
        print("⚠️  Warning: Swagger merge may have failed\n")
except Exception as e:
    print(f"⚠️  Warning: Could not merge swagger files: {e}\n")

# Create the Flask app
app = create_app('ProductionConfig')

print(f"📱 Flask app created")

# Create database tables
with app.app_context():
    print("🔨 Creating database tables...")
    try:
        db.create_all()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

print("\n" + "=" * 60)
print("Flask Application Ready")
print("=" * 60 + "\n")