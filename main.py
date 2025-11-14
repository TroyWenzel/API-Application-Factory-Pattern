from app import create_app
from app.models import db

main = create_app('DevelopmentConfig')

with main.app_context():
    print(main.url_map)  # This will show all registered routes
    db.create_all()
    
main.run(debug=True)
