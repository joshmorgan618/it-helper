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

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default='user')
    tier_level = db.Column(db.String, nullable=False, default='tier1')
    specialization = db.Column(db.String, nullable=True)
    building = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generated_user_id():
        """Generate unique user ID"""
        return f"USR-{uuid.uuid4().hex[:8].upper()}"   

class TicketAssignments(db.Model):
    __tablename__ = 'ticket_assignments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.String, db.ForeignKey('tickets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    role = db.Column(db.String, nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)







class Classifications(db.Model):
    __tablename__ = 'classifications'


    ticket_id = db.Column(db.String, db.ForeignKey('tickets.id'), primary_key=True)
    category = db.Column(db.String, nullable=False)
    urgency = db.Column(db.String, nullable=False)
    expertise_level = db.Column(db.String, nullable=False)
    reasoning = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Diagnostics(db.Model):
    __tablename__ = 'diagnostics'

    ticket_id = db.Column(db.String, db.ForeignKey('tickets.id'), primary_key=True)
    diagnosis = db.Column(db.String, nullable=False)
    potential_causes = db.Column(db.JSON, nullable=False)
    recommended_tests = db.Column(db.JSON, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Solutions(db.Model):
    __tablename__ = 'solutions'
    ticket_id = db.Column(db.String, db.ForeignKey('tickets.id'), primary_key=True)
    solution = db.Column(db.String, nullable=False)
    tools_needed = db.Column(db.JSON, nullable=False)
    estimated_time = db.Column(db.String, nullable=False)
    confidence = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Workflow_log(db.Model):
    __tablename__ = 'workflow_log'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.String, db.ForeignKey('tickets.id'), nullable=False)
    log_entries = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



    

