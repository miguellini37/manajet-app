"""
SQLAlchemy ORM Models for PostgreSQL
Matches the existing data model structure from jet_manager.py
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from db_config import Base

class CustomerModel(Base):
    __tablename__ = 'customers'

    customer_id = Column(String(50), primary_key=True)
    name = Column(String(200), nullable=False)
    company = Column(String(200))
    email = Column(String(200))
    phone = Column(String(50))
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UserModel(Base):
    __tablename__ = 'users'

    user_id = Column(String(50), primary_key=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # admin, customer, crew, mechanic
    related_id = Column(String(50))  # Links to customer_id, crew_id, etc.
    email = Column(String(200))
    apple_user_id = Column(String(255), unique=True, index=True)  # Apple Sign In user identifier
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PassengerModel(Base):
    __tablename__ = 'passengers'

    passenger_id = Column(String(50), primary_key=True)
    name = Column(String(200), nullable=False)
    passport_number = Column(String(100))
    nationality = Column(String(100))
    passport_expiry = Column(String(50))
    contact = Column(String(200))
    customer_id = Column(String(50), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class CrewModel(Base):
    __tablename__ = 'crew'

    crew_id = Column(String(50), primary_key=True)
    name = Column(String(200), nullable=False)
    role = Column(String(100))  # Pilot, Co-pilot, Flight Attendant
    license_number = Column(String(100))
    license_expiry = Column(String(50))
    contact = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class JetModel(Base):
    __tablename__ = 'jets'

    jet_id = Column(String(50), primary_key=True)
    model = Column(String(200), nullable=False)
    registration = Column(String(100), unique=True)
    capacity = Column(Integer)
    status = Column(String(50))  # Available, In Flight, Maintenance
    customer_id = Column(String(50), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class FlightModel(Base):
    __tablename__ = 'flights'

    flight_id = Column(String(50), primary_key=True)
    jet_id = Column(String(50), nullable=False, index=True)
    departure = Column(String(200), nullable=False)
    destination = Column(String(200), nullable=False)
    departure_time = Column(String(50))
    arrival_time = Column(String(50))
    passenger_ids = Column(JSON)  # Store as JSON array
    crew_ids = Column(JSON)  # Store as JSON array
    status = Column(String(50))  # Scheduled, In Progress, Completed, Cancelled
    customer_id = Column(String(50), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class MaintenanceModel(Base):
    __tablename__ = 'maintenance'

    maintenance_id = Column(String(50), primary_key=True)
    jet_id = Column(String(50), nullable=False, index=True)
    maintenance_type = Column(String(200))  # Routine, Engine, Avionics, etc.
    scheduled_date = Column(String(50))
    completion_date = Column(String(50))
    description = Column(Text)
    status = Column(String(50))  # Scheduled, In Progress, Completed
    performed_by = Column(String(200))
    customer_id = Column(String(50), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
