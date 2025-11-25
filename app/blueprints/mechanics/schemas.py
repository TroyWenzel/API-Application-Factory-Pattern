from app.extensions import ma
from app.models import Mechanics
from marshmallow import fields

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics
        load_instance = True
        exclude = ('password',)

class LoginSchema(ma.Schema):
    #Schema for mechanic login - only email and password
    email = fields.Email(required=True)
    password = fields.Str(required=True)


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
login_schema = LoginSchema()