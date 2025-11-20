from app import create_app
from app.models import db

main = create_app('DevelopmentConfig')

with main.app_context():
    #print(main.url_map) 
    #db.drop_all()
    db.create_all()
    
main.run(debug=True)
