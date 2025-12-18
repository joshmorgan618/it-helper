from os import getenv
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from models import db, Ticket, Classifications, Diagnostics, Solutions, Workflow_log
from anthropic import Anthropic 
from redis_client import RedisDB  
from overseer import Overseer 

load_dotenv()

app = Flask(__name__)
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


@app.route('/api/tickets', methods=['POST'])
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
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return {"error": "Ticket not found"}, 404

    # Fetch related data
    classification = Classifications.query.filter_by(ticket_id=ticket_id).first()
    diagnostic = Diagnostics.query.filter_by(ticket_id=ticket_id).first()
    solution = Solutions.query.filter_by(ticket_id=ticket_id).first()
    log = Workflow_log.query.filter_by(ticket_id=ticket_id).first()

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
        "workflow_log": log.log_entries if log else []
    }
    

if __name__ == '__main__':
    app.run(debug=True)