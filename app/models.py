from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Column, ForeignKey, Table, Float, Integer
from datetime import date

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

ticket_mechanic = Table(
    'ticket_mechanic',
    Base.metadata,
    Column('ticket_id', Integer, ForeignKey('service_tickets.id'), primary_key=True),
    Column('mechanic_id', Integer, ForeignKey('mechanics.id'), primary_key=True)
)
# Customers table
class Customers(Base):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(350), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=True)

# Relationship: one customer can have many service tickets
    service_tickets: Mapped[list["ServiceTickets"]] = relationship(back_populates="customer")

# Service Tickets table
class ServiceTickets(Base):
    __tablename__ = 'service_tickets'
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    service_desc: Mapped[str] = mapped_column(String(1000), nullable=False)
    VIN: Mapped[str] = mapped_column(String(17), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Relationships
    customer: Mapped["Customers"] = relationship(back_populates="service_tickets")
    mechanics: Mapped[list["Mechanics"]] = relationship(secondary=ticket_mechanic, back_populates="service_tickets")

# Mechanics table
class Mechanics(Base):
    __tablename__ = 'mechanics'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(350), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(500), nullable=True)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Relationship: one mechanic can work on many service tickets
    service_tickets: Mapped[list["ServiceTickets"]] = relationship(secondary=ticket_mechanic, back_populates="mechanics")