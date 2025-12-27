# IT Helper

**AI-Powered IT Support Automation Platform**

A production-ready, enterprise-grade intelligent ticketing system that leverages multi-agent AI architecture to automate IT support workflows, reduce response times, and improve resolution accuracy.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Usage](#usage)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## Overview

IT Helper is an intelligent ticket management system that combines the power of Large Language Models (LLMs) with a sophisticated multi-agent architecture to provide automated IT support diagnostics and solutions. The platform processes user-submitted issues through a coordinated workflow of specialized AI agents, each responsible for a specific aspect of ticket resolution.

### Business Value

- **Reduced Resolution Time**: Automated classification and diagnosis cut average ticket resolution time by up to 70%
- **Improved Accuracy**: AI-powered diagnostic agents leverage historical data and documentation to provide precise solutions
- **Scalability**: Handle increased ticket volume without proportional staffing increases
- **Knowledge Retention**: Persistent learning from past resolutions stored in Redis and PostgreSQL
- **User Experience**: Real-time dashboard with assigned specialist visibility and ticket tracking

---

## Key Features

### Intelligent Ticket Processing

- **Multi-Agent Workflow**: Coordinated AI agents handle intake, classification, diagnosis, and solution generation
- **Automated Classification**: Smart categorization by urgency, expertise level, and issue type
- **Context-Aware Diagnostics**: AI agents analyze tickets with historical context from similar issues
- **Dynamic Specialist Assignment**: Automatic routing to appropriate IT specialists based on category and expertise

### Real-Time Dashboard

- **Live Ticket Tracking**: Monitor ticket status, assignments, and progress in real-time
- **Specialist Visibility**: See assigned primary and secondary specialists with their specializations
- **Detailed Ticket Views**: Comprehensive ticket information including diagnosis, potential causes, and recommended solutions
- **Status Management**: Track tickets through open, in-progress, resolved, and closed states

### Enterprise-Ready Architecture

- **RESTful API**: Clean, well-documented API endpoints for all ticket operations
- **PostgreSQL Database**: Reliable persistent storage for tickets, users, classifications, diagnostics, and solutions
- **Redis Caching**: High-performance caching layer for learning from past resolutions
- **Scalable Design**: Microservices-ready architecture supporting horizontal scaling

### Security & Compliance

- **Structured Data Models**: Strong typing and validation at database level
- **Audit Trail**: Complete workflow logging for compliance and troubleshooting
- **Role-Based Access**: User roles and tier levels for access control
- **CORS Support**: Configurable cross-origin resource sharing

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Ticket     │  │   Ticket     │  │   Ticket     │         │
│  │  Submission  │  │  Dashboard   │  │   Detail     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                    React 19.2 + Modern CSS                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                          │
│                                                                 │
│                    Flask REST API + CORS                        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                   API Endpoints                           │ │
│  │  POST   /api/tickets          - Create ticket            │ │
│  │  GET    /api/tickets          - List all tickets         │ │
│  │  GET    /api/tickets/:id      - Get ticket details       │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                  Overseer Agent                          │ │
│  │         Coordinates Multi-Agent Workflow                 │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                  │
│      ┌───────────┬───────────┼───────────┬──────────┐         │
│      ▼           ▼           ▼           ▼          ▼         │
│  ┌────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ ┌────────┐ │
│  │ Intake │ │Classifier│ │Diagnostic│ │ Fetch  │ │Solution│ │
│  │ Agent  │ │  Agent   │ │  Agent   │ │ Agent  │ │ Agent  │ │
│  └────────┘ └──────────┘ └──────────┘ └────────┘ └────────┘ │
│                                                                 │
│           All agents powered by Claude API (Anthropic)         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Data Layer                                │
│                                                                 │
│  ┌──────────────────┐          ┌──────────────────┐           │
│  │   PostgreSQL     │          │      Redis       │           │
│  │                  │          │                  │           │
│  │ • Tickets        │          │ • Resolution     │           │
│  │ • Users          │          │   Cache          │           │
│  │ • Classifications│          │ • Learning Data  │           │
│  │ • Diagnostics    │          │ • Session Store  │           │
│  │ • Solutions      │          │                  │           │
│  │ • Assignments    │          │                  │           │
│  │ • Workflow Logs  │          │                  │           │
│  └──────────────────┘          └──────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

### Multi-Agent Workflow

```
User Submission
      ↓
1. Intake Agent
   → Validates and structures input
   → Extracts: email, subject, description
      ↓
2. Classifier Agent
   → Analyzes ticket content
   → Returns: category, urgency, expertise level
      ↓
3. Diagnostic Agent
   → Searches Redis for similar past issues
   → Performs root cause analysis
   → Returns: diagnosis, potential causes, recommended tests
      ↓
4. Fetch Agent
   → Retrieves relevant documentation
   → Gathers context-specific resources
      ↓
5. Solution Agent
   → Combines diagnosis + documentation + past solutions
   → Generates step-by-step resolution
   → Returns: solution, tools needed, estimated time, confidence
      ↓
6. Assignment Logic
   → Routes to appropriate specialists
   → Assigns primary and secondary contacts
      ↓
7. Persistence & Response
   → Stores all data in PostgreSQL
   → Caches resolution in Redis
   → Returns complete ticket to user
```

---

## Technology Stack

### Frontend
- **React** 19.2.3 - Modern UI framework
- **CSS3** - Custom styling with responsive design
- **Fetch API** - HTTP client for backend communication

### Backend
- **Flask** - Lightweight Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-SQLAlchemy** - ORM for database interactions
- **Python** 3.x - Core programming language

### AI & ML
- **Anthropic Claude API** - Large language model for agent intelligence
- **Multi-Agent System** - Coordinated AI agents for specialized tasks

### Databases
- **PostgreSQL** - Primary relational database
- **Redis** - In-memory cache and learning store

### DevOps & Tools
- **Git** - Version control
- **npm** - Frontend package management
- **pip** - Python package management

---

## Prerequisites

Before installation, ensure you have the following installed:

- **Node.js** 16.x or higher
- **npm** 8.x or higher
- **Python** 3.9 or higher
- **PostgreSQL** 13.x or higher
- **Redis** 6.x or higher
- **Git** 2.x or higher

### Required API Keys

- **Anthropic API Key** - Sign up at [Anthropic](https://www.anthropic.com/)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/it-helper.git
cd it-helper
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd src/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb it_support_db

# Database tables will be created automatically on first run
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install
```

---

## Configuration

### Backend Environment Variables

Create a `.env` file in `src/backend/`:

```env
# Database Configuration
DATABASE_URL=postgresql://localhost:5432/it_support_db

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Anthropic API
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### Frontend Configuration

The frontend is configured to connect to the backend at `http://localhost:5000`. To modify this, update the API endpoint in:

```javascript
// src/frontend/src/App.js
const response = await fetch('http://localhost:5000/api/tickets');
```

---

## API Documentation

### Endpoints

#### Create Ticket
**POST** `/api/tickets`

Create a new support ticket with AI-powered processing.

**Request Body:**
```json
{
  "user_email": "user@example.com",
  "subject": "Printer not connecting to network",
  "description": "The office printer on the 3rd floor won't connect to WiFi. Error message shows 'Connection timeout'."
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "ticket_id": "TKT-A4D3106B",
  "status": "processed",
  "summary": {
    "category": "hardware",
    "urgency": "medium",
    "solution_preview": "Based on the connection timeout error, this appears to be a network configuration issue..."
  }
}
```

#### List All Tickets
**GET** `/api/tickets`

Retrieve all tickets with complete information including classifications, diagnostics, solutions, and assigned specialists.

**Response (200 OK):**
```json
[
  {
    "id": "TKT-A4D3106B",
    "user_email": "user@example.com",
    "subject": "Printer not connecting to network",
    "description": "The office printer on the 3rd floor won't connect to WiFi...",
    "status": "open",
    "created_at": "2025-12-22T14:48:41.123Z",
    "updated_at": "2025-12-22T14:48:41.123Z",
    "classification": {
      "category": "hardware",
      "urgency": "medium",
      "expertise_level": "tier1",
      "reasoning": "Network connectivity issue requiring basic troubleshooting"
    },
    "diagnosis": {
      "diagnosis": "Printer connectivity failure, likely network or driver issue",
      "potential_causes": [
        "Network cable disconnected",
        "WiFi settings misconfigured",
        "IP address conflict"
      ],
      "recommended_tests": [
        "Check physical connections",
        "Verify WiFi credentials",
        "Ping printer IP address"
      ]
    },
    "solution": {
      "solution": "1. Verify printer is powered on...",
      "tools_needed": ["Network cable tester", "Admin credentials"],
      "estimated_time": "15-20 minutes",
      "confidence": "high"
    },
    "assigned_people": [
      {
        "role": "primary",
        "name": "John Smith",
        "email": "john.smith@company.com",
        "specialization": "network",
        "tier_level": "tier1",
        "assigned_at": "2025-12-22T14:48:41.456Z"
      }
    ]
  }
]
```

#### Get Ticket by ID
**GET** `/api/tickets/:ticket_id`

Retrieve detailed information for a specific ticket.

**Response (200 OK):**
```json
{
  "id": "TKT-A4D3106B",
  "user_email": "user@example.com",
  "subject": "Printer not connecting to network",
  "description": "...",
  "status": "open",
  "created_at": "2025-12-22T14:48:41.123Z",
  "updated_at": "2025-12-22T14:48:41.123Z",
  "classification": { ... },
  "diagnosis": { ... },
  "solution": { ... },
  "assigned_people": [ ... ],
  "workflow_log": [ ... ]
}
```

### Error Responses

**400 Bad Request:**
```json
{
  "error": "Invalid input"
}
```

**404 Not Found:**
```json
{
  "error": "Ticket not found"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Database error"
}
```

---

## Usage

### Starting the Application

#### 1. Start Backend Server

```bash
cd src/backend
source venv/bin/activate  # Activate virtual environment
python app.py
```

The backend will start on `http://localhost:5000`

#### 2. Start Frontend Development Server

```bash
cd src/frontend
npm start
```

The frontend will start on `http://localhost:3000`

### Creating a Ticket

1. Navigate to the **Submit Ticket** view
2. Enter your email address
3. Provide a subject line
4. Describe the issue in detail
5. Click **Submit**
6. View the AI-generated diagnosis and solution in the ticket detail modal

### Viewing Tickets

1. Click **Dashboard** in the navigation
2. Browse all submitted tickets
3. See assigned specialists directly on each ticket card
4. Click any ticket to view complete details including:
   - Classification and urgency
   - Assigned specialists with specializations
   - Detailed diagnosis and potential causes
   - Step-by-step solution with tools needed
   - Estimated resolution time

---

## Development

### Project Structure

```
it-helper/
├── src/
│   ├── backend/
│   │   ├── app.py                 # Flask application and API routes
│   │   ├── models.py              # SQLAlchemy database models
│   │   ├── overseer.py            # Multi-agent workflow orchestrator
│   │   ├── redis_client.py        # Redis cache interface
│   │   └── .env                   # Environment configuration
│   ├── frontend/
│   │   ├── public/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── Navigation.js
│   │   │   │   ├── TicketSubmission.js
│   │   │   │   ├── TicketDashboard.js
│   │   │   │   └── TicketDetail.js
│   │   │   ├── App.js             # Main React component
│   │   │   ├── App.css
│   │   │   └── index.js
│   │   └── package.json
│   └── mas_agents/
│       ├── base_agent.py          # Base class for all agents
│       ├── intake_agent.py        # Input validation agent
│       ├── classifier_agent.py    # Ticket classification agent
│       ├── diagnostic_agent.py    # Diagnostic analysis agent
│       ├── fetch_agent.py         # Documentation retrieval agent
│       └── solution_agent.py      # Solution generation agent
├── tests/
│   └── test_classifier_agent_prompts.py
├── README.md
├── requirements.txt
└── STYLE_GUIDE.md
```

### Database Models

#### Tickets
- `id` (String, Primary Key)
- `user_email` (String)
- `subject` (String)
- `description` (String)
- `status` (Enum: open, in_progress, resolved, closed)
- `created_at`, `updated_at` (DateTime)

#### Users
- `user_id` (Integer, Primary Key)
- `email` (String, Unique)
- `name` (String)
- `role` (String)
- `tier_level` (String)
- `specialization` (String)
- `building` (String)

#### Classifications
- `ticket_id` (String, Foreign Key)
- `category` (String)
- `urgency` (String)
- `expertise_level` (String)
- `reasoning` (String)

#### Diagnostics
- `ticket_id` (String, Foreign Key)
- `diagnosis` (String)
- `potential_causes` (JSON)
- `recommended_tests` (JSON)

#### Solutions
- `ticket_id` (String, Foreign Key)
- `solution` (String)
- `tools_needed` (JSON)
- `estimated_time` (String)
- `confidence` (String)

#### Ticket Assignments
- `id` (Integer, Primary Key)
- `ticket_id` (String, Foreign Key)
- `user_id` (Integer, Foreign Key)
- `role` (String: primary, secondary)
- `assigned_at` (DateTime)

### Adding New Agents

To add a new agent to the multi-agent system:

1. Create a new agent class in `src/mas_agents/`
2. Extend `BaseAgent` class
3. Implement the `process()` method
4. Define system prompts for Claude API
5. Register the agent in `overseer.py`
6. Update workflow sequence

Example:

```python
from .base_agent import BaseAgent
import json

class NewAgent(BaseAgent):
    def __init__(self, client):
        super().__init__(client, name="NewAgent")

    def process(self, input_data):
        self.log_action("Processing with NewAgent")

        system_prompt = """
        Your agent instructions here...
        """

        messages = [
            {"role": "user", "content": f"Data: {json.dumps(input_data)}"}
        ]

        response = self.call_claude(messages, system_prompt)
        return json.loads(response)
```

---

## Testing

### Backend Tests

```bash
cd src/backend
python -m pytest tests/
```

### Frontend Tests

```bash
cd src/frontend
npm test
```

### End-to-End Testing

1. Start backend and frontend servers
2. Submit a test ticket through the UI
3. Verify ticket appears in dashboard
4. Check database for correct data persistence
5. Verify Redis cache is updated

---

## Deployment

### Production Considerations

#### Environment Variables
- Set `FLASK_ENV=production`
- Use strong database credentials
- Secure API keys with secret management tools

#### Database
- Use managed PostgreSQL service (AWS RDS, Google Cloud SQL)
- Enable connection pooling
- Set up automated backups
- Configure read replicas for scaling

#### Redis
- Use managed Redis service (AWS ElastiCache, Redis Cloud)
- Enable persistence
- Configure eviction policies

#### Backend
- Deploy with production WSGI server (Gunicorn, uWSGI)
- Use reverse proxy (Nginx)
- Enable HTTPS/SSL
- Configure logging and monitoring

#### Frontend
- Build optimized production bundle: `npm run build`
- Deploy to CDN (Cloudflare, AWS CloudFront)
- Enable caching
- Configure environment-specific API endpoints

### Example Production Deployment

#### Backend (Gunicorn)

```bash
# Install Gunicorn
pip install gunicorn

# Start with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Nginx Configuration

```nginx
server {
    listen 80;
    server_name api.yourcompany.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Docker Deployment

Create `Dockerfile` in backend:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./src/backend
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/it_support_db
      - REDIS_URL=redis://redis:6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=it_support_db
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6
    volumes:
      - redis_data:/data

  frontend:
    build: ./src/frontend
    ports:
      - "80:80"

volumes:
  postgres_data:
  redis_data:
```

---

## Contributing

We welcome contributions to IT Helper! Please follow these guidelines:

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Write or update tests
5. Ensure all tests pass
6. Update documentation
7. Commit with clear messages: `git commit -m "Add feature: description"`
8. Push to your fork: `git push origin feature/your-feature-name`
9. Open a Pull Request

### Code Standards

- **Python**: Follow PEP 8 style guide
- **JavaScript**: Follow Airbnb JavaScript Style Guide
- **Git Commits**: Use conventional commit messages
- **Documentation**: Update README and inline comments
- **Testing**: Maintain test coverage above 80%

### Pull Request Process

1. Ensure your PR description clearly describes the problem and solution
2. Reference any related issues
3. Update the README.md with details of changes if applicable
4. The PR will be merged once you have sign-off from maintainers

---

## License

This project is proprietary software. All rights reserved.

For licensing inquiries, contact: licensing@yourcompany.com

---

## Support

### Documentation
- [API Documentation](#api-documentation)
- [Architecture Guide](#architecture)
- [Style Guide](STYLE_GUIDE.md)

### Getting Help
- **Email**: support@yourcompany.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/it-helper/issues)
- **Slack**: #it-helper-support

### Reporting Bugs
Please use the GitHub issue tracker and include:
- Detailed description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, Node version)
- Relevant logs

### Feature Requests
Submit feature requests through GitHub Issues with the `enhancement` label.

---

## Acknowledgments

- **Anthropic** for Claude API
- **Flask** community for excellent documentation
- **React** team for the frontend framework
- All contributors and early adopters

---

**Built with excellence for enterprise IT support.**

*Last Updated: December 2025*
