from app.extensions import ma
from app.models import Inventory, Parts

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True

class PartsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Parts
        load_instance = True
        include_fk = True

# Schema instances
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

part_schema = PartsSchema()
parts_schema = PartsSchema(many=True)