from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import db
from app.blueprints.service_tickets.schemas import service_ticket_schema

service_tickets_bp = Blueprint('service_tickets', __name__)


@service_tickets_bp.route('', methods=['POST'])
def create_service_ticket():
    try:
        new_ticket = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201


@service_tickets_bp.route('', methods=['GET'])
def read_tickets():
    tickets = ServiceTickets.query.all()
    return tickets_schema.jsonify(tickets), 200


@service_tickets_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404

    try:
        updated = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for attr in ['customer_id', 'mechanic_id', 'description', 'status']:
        if hasattr(updated, attr):
            setattr(ticket, attr, getattr(updated, attr))

    db.session.commit()
    return ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'message': 'Ticket deleted'}), 200