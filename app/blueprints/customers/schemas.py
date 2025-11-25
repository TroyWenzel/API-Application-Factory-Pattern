from app.extensions import ma
from app.models import Customers
from marshmallow import fields

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customers
        load_instance = True
        
class CustomerLoginSchema(ma.Schema):
    #Schema for customer login - only email and password
    email = fields.Email(required=True)
    password = fields.Str(required=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

customer_login_schema = CustomerLoginSchema()
