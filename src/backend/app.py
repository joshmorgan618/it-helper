from os import getenv
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from models import db, Ticket, Classifications, Diagnostics, Solutions, Workflow_log, User
from anthropic import Anthropic
from redis_client import RedisDB
from overseer import Overseer
from flask_cors import CORS
from models import TicketAssignments

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

anthropic_client = Anthropic(api_key=getenv('ANTHROPIC_API_KEY'))
redis_client = RedisDB(getenv('REDIS_URL'))
overseer = Overseer(anthropic_client, redis_client)


# Create tables
with app.app_context():
    db.create_all()
    print("Database tables created!")


@app.route('/api/tickets', methods=['GET', 'POST'])
def tickets():
    if request.method == 'GET':
        # Fetch all tickets with related data
        all_tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
        tickets_data = []

        for ticket in all_tickets:
            classification = Classifications.query.filter_by(ticket_id=ticket.id).first()
            diagnostic = Diagnostics.query.filter_by(ticket_id=ticket.id).first()
            solution = Solutions.query.filter_by(ticket_id=ticket.id).first()

            # Fetch assignments with user details
            assignments = TicketAssignments.query.filter_by(ticket_id=ticket.id).all()
            assigned_people = []
            for assignment in assignments:
                user = db.session.get(User, assignment.user_id)
                if user:
                    assigned_people.append({
                        "role": assignment.role,
                        "name": user.name,
                        "email": user.email,
                        "specialization": user.specialization,
                        "tier_level": user.tier_level,
                        "assigned_at": assignment.assigned_at.isoformat()
                    })

            ticket_data = {
                "id": ticket.id,
                "user_email": ticket.user_email,
                "subject": ticket.subject,
                "description": ticket.description,
                "status": ticket.status.value,
                "created_at": ticket.created_at.isoformat(),
                "updated_at": ticket.updated_at.isoformat(),
                "classification": {
                    "category": classification.category,
                    "urgency": classification.urgency,
                    "expertise_level": classification.expertise_level,
                    "reasoning": classification.reasoning
                } if classification else None,
                "diagnosis": {
                    "diagnosis": diagnostic.diagnosis,
                    "potential_causes": diagnostic.potential_causes,
                    "recommended_tests": diagnostic.recommended_tests
                } if diagnostic else None,
                "solution": {
                    "solution": solution.solution,
                    "tools_needed": solution.tools_needed,
                    "estimated_time": solution.estimated_time,
                    "confidence": solution.confidence
                } if solution else None,
                "assigned_people": assigned_people
            }
            tickets_data.append(ticket_data)

        return jsonify(tickets_data), 200

    # POST method - create ticket
def create_ticket():
    data = request.get_json()
    if not data or not all(k in data for k in ('user_email', 'subject', 'description')):
        return {"error": "Invalid input"}, 400

    # Process ticket through overseer
    overseer_result = overseer.process_ticket(data)
    if not overseer_result or "error" in overseer_result:
        return {"error": "Failed to process ticket"}, 500

    # Extract results
    intake_result = overseer_result["intake_result"]
    classification_result = overseer_result["classification"]
    diagnosis_result = overseer_result["diagnosis"]
    fetch_result = overseer_result["fetched_data"]
    solution_result = overseer_result["solution"]
    workflow_log = overseer_result["workflow_log"]

    try:
        # Create ticket with cleaned data from intake
        ticket = Ticket(
            id=Ticket.generate_id(),
            user_email=intake_result['user_email'],
            subject=intake_result['subject'],
            description=intake_result['description']
        )
        db.session.add(ticket)
        db.session.flush()
        
        # Create classification
        classification = Classifications(
            ticket_id=ticket.id,
            category=classification_result["category"],
            urgency=classification_result["urgency"],
            expertise_level=classification_result["expertise_level"],
            reasoning=classification_result["reasoning"]
        )
        db.session.add(classification)
        
        # Create diagnostic
        diagnostic = Diagnostics(
            ticket_id=ticket.id,
            diagnosis=diagnosis_result["diagnosis"],
            potential_causes=diagnosis_result["potential_causes"],
            recommended_tests=diagnosis_result["recommended_tests"]
        )
        db.session.add(diagnostic)
        
        # Create solution
        solution = Solutions(
            ticket_id=ticket.id,
            solution=solution_result["solution"],
            tools_needed=solution_result["tools_needed"],
            estimated_time=solution_result["estimated_time"],
            confidence=solution_result["confidence"]
        )
        db.session.add(solution)

        assignments = overseer_result.get("assignments", {})
        if assignments.get('primary'):
            primary_assignment = TicketAssignments(
                ticket_id=ticket.id,
                user_id=assignments['primary']['user_id'],
                role='primary'
            )
            db.session.add(primary_assignment)

        if assignments.get('secondary'):
            secondary_assignment = TicketAssignments(
                ticket_id=ticket.id,
                user_id=assignments['secondary']['user_id'],
                role='secondary'
            )
            db.session.add(secondary_assignment)
    
        # Create workflow log
        log = Workflow_log(
            ticket_id=ticket.id,
            log_entries=workflow_log
        )
        db.session.add(log)
        
        # Commit all changes
        db.session.commit()

        # Store in Redis for learning
        redis_client.store_resolution(
            ticket_id=ticket.id,
            category=classification_result["category"],
            solution=solution_result["solution"],
            success=True
        )
        
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return {"error": "Database error"}, 500
    
    return {
        "success": True,
        "ticket_id": ticket.id,
        "status": "processed",
        "summary": {
            "category": classification_result['category'],
            "urgency": classification_result['urgency'],
            "solution_preview": solution_result['solution'][:100] + "..."
        }
    }, 201


@app.route('/api/tickets/<ticket_id>', methods=['GET'])
def fetch_ticket(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)
    if not ticket:
        return {"error": "Ticket not found"}, 404

    # Fetch related data
    classification = Classifications.query.filter_by(ticket_id=ticket_id).first()
    diagnostic = Diagnostics.query.filter_by(ticket_id=ticket_id).first()
    solution = Solutions.query.filter_by(ticket_id=ticket_id).first()
    log = Workflow_log.query.filter_by(ticket_id=ticket_id).first()

    # Fetch assignments with user details
    assignments = TicketAssignments.query.filter_by(ticket_id=ticket_id).all()
    assigned_people = []
    for assignment in assignments:
        user = db.session.get(User, assignment.user_id)
        if user:
            assigned_people.append({
                "role": assignment.role,
                "name": user.name,
                "email": user.email,
                "specialization": user.specialization,
                "tier_level": user.tier_level,
                "assigned_at": assignment.assigned_at.isoformat()
            })

    return {
        "id": ticket.id,
        "user_email": ticket.user_email,
        "subject": ticket.subject,
        "description": ticket.description,
        "status": ticket.status.value,
        "created_at": ticket.created_at.isoformat(),
        "updated_at": ticket.updated_at.isoformat(),
        "classification": {
            "category": classification.category if classification else None,
            "urgency": classification.urgency if classification else None,
            "expertise_level": classification.expertise_level if classification else None,
            "reasoning": classification.reasoning if classification else None,
            "created_at": classification.created_at.isoformat() if classification else None,
            "updated_at": classification.updated_at.isoformat() if classification else None
        } if classification else None,
        "diagnosis": {
            "diagnosis": diagnostic.diagnosis if diagnostic else None,
            "potential_causes": diagnostic.potential_causes if diagnostic else None,
            "recommended_tests": diagnostic.recommended_tests if diagnostic else None,
            "created_at": diagnostic.created_at.isoformat() if diagnostic else None,
            "updated_at": diagnostic.updated_at.isoformat() if diagnostic else None
        } if diagnostic else None,
        "solution": {
            "solution": solution.solution if solution else None,
            "tools_needed": solution.tools_needed if solution else None,
            "estimated_time": solution.estimated_time if solution else None,
            "confidence": solution.confidence if solution else None,
            "created_at": solution.created_at.isoformat() if solution else None,
            "updated_at": solution.updated_at.isoformat() if solution else None
        } if solution else None,
        "assigned_people": assigned_people,
        "workflow_log": log.log_entries if log else []
    }
    

if __name__ == '__main__':
    app.run(debug=True)
    