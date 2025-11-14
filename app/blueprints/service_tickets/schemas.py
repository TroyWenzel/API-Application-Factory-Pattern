from app.extensions import ma
from app.models import ServiceTickets


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTickets
        load_instance = True
        include_fk = True




service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)