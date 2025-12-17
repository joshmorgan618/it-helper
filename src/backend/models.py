import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
import uuid

db = SQLAlchemy()

class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.String, primary_key=True)    
    user_email = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum(TicketStatus), default=TicketStatus.OPEN)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def generate_id():
        """Generate unique ticket ID"""
        return f"TKT-{uuid.uuid4().hex[:8].upper()}"   

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generated_user_id():
        """Generate unique user ID"""
        return f"USR-{uuid.uuid4().hex[:8].upper()}"   

    

