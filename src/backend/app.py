
from os import getenv
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from models import db, Ticket


load_dotenv()  # Load .env file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()
    print("Database tables created!")


@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json()
    if not data or not all(k in data for k in ('user_email', 'subject', 'description')):
        return {"error": "Invalid input"}, 400
    ticket = Ticket(
        id=Ticket.generate_id(),
        user_email=data.get('user_email'),
        subject=data.get('subject'),
        description=data.get('description')
    )
    try :
        db.session.add(ticket)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": "Database error"}, 500
    return {"success": True, "ticket_id": ticket.id}, 201

@app.route('/api/tickets/<ticket_id>', methods=['GET'])
def fetch_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return {"error": "Ticket not found"}, 404
    return {
        "id": ticket.id,
        "user_email": ticket.user_email,
        "subject": ticket.subject,
        "description": ticket.description,
        "status": ticket.status.value,
        "created_at": ticket.created_at.isoformat(),
        "updated_at": ticket.updated_at.isoformat()
    }
    

if __name__ == '__main__':
    app.run(debug=True)