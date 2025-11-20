from app.extensions import ma
from app.models import ServiceTickets


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTickets
        load_instance = True
        include_fk = True
        exclude = ('mechanics',) # Exclude the relationship to avoid serialization issues




service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)