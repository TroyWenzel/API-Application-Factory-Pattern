from app.extensions import ma
from app.models import Customers

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customers
        load_instance = True

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)