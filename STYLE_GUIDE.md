# IT Helper Style Guide

**Version 1.0 | Last Updated: December 2025**

---

## Table of Contents

1. [Introduction](#introduction)
2. [General Principles](#general-principles)
3. [Python Style Guide](#python-style-guide)
4. [JavaScript/React Style Guide](#javascriptreact-style-guide)
5. [CSS Style Guide](#css-style-guide)
6. [Git Conventions](#git-conventions)
7. [Documentation Standards](#documentation-standards)
8. [API Design Principles](#api-design-principles)
9. [Database Conventions](#database-conventions)
10. [Testing Standards](#testing-standards)
11. [Security Best Practices](#security-best-practices)
12. [Code Review Guidelines](#code-review-guidelines)
13. [Performance Standards](#performance-standards)
14. [Accessibility Standards](#accessibility-standards)
15. [Error Handling](#error-handling)

---

## Introduction

This style guide establishes coding standards, best practices, and conventions for the IT Helper project. All contributors must adhere to these guidelines to ensure code consistency, maintainability, and quality across the codebase.

### Purpose

- **Consistency**: Uniform code style across all components
- **Maintainability**: Easy to read, understand, and modify
- **Quality**: Reduce bugs and technical debt
- **Collaboration**: Smooth team collaboration and code reviews
- **Scalability**: Support growth and evolution of the codebase

### Enforcement

- All code must pass linting checks before merge
- Code reviews enforce style guide compliance
- Automated CI/CD pipelines validate standards
- Non-compliant code will not be merged to main branch

---

## General Principles

### Code Philosophy

1. **Clarity Over Cleverness**
   - Write code that is easy to understand, not impressive
   - Prioritize readability over brevity
   - Use descriptive names over short, cryptic ones

2. **DRY (Don't Repeat Yourself)**
   - Extract repeated code into reusable functions
   - Create utilities for common operations
   - Avoid copy-paste programming

3. **SOLID Principles**
   - Single Responsibility: One function, one purpose
   - Open/Closed: Open for extension, closed for modification
   - Liskov Substitution: Subtypes must be substitutable
   - Interface Segregation: Many specific interfaces over one general
   - Dependency Inversion: Depend on abstractions, not concretions

4. **KISS (Keep It Simple, Stupid)**
   - Simple solutions over complex ones
   - Avoid premature optimization
   - Refactor when complexity grows

5. **YAGNI (You Aren't Gonna Need It)**
   - Don't build features before they're needed
   - Avoid speculative generalization
   - Focus on current requirements

### File Organization

```
src/
├── backend/
│   ├── app.py                    # Main application entry point
│   ├── models.py                 # Database models
│   ├── config.py                 # Configuration management
│   ├── utils/                    # Utility functions
│   │   ├── validators.py
│   │   └── helpers.py
│   └── tests/                    # Backend tests
│       ├── test_models.py
│       └── test_api.py
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── hooks/                # Custom React hooks
│   │   ├── utils/                # JavaScript utilities
│   │   ├── styles/               # Global styles
│   │   └── tests/                # Frontend tests
│   └── public/                   # Static assets
└── mas_agents/
    ├── base_agent.py             # Base agent class
    ├── intake_agent.py           # Specialized agents
    └── tests/                    # Agent tests
```

### Naming Conventions

#### Python
- **Files**: `snake_case.py` (e.g., `base_agent.py`)
- **Classes**: `PascalCase` (e.g., `ClassifierAgent`)
- **Functions/Methods**: `snake_case` (e.g., `process_ticket`)
- **Variables**: `snake_case` (e.g., `ticket_id`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **Private**: Prefix with `_` (e.g., `_internal_method`)

#### JavaScript/React
- **Files**: `PascalCase.js` for components (e.g., `TicketDashboard.js`)
- **Files**: `camelCase.js` for utilities (e.g., `apiHelpers.js`)
- **Components**: `PascalCase` (e.g., `TicketDetail`)
- **Functions**: `camelCase` (e.g., `handleSubmit`)
- **Variables**: `camelCase` (e.g., `ticketId`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `API_ENDPOINT`)

#### CSS
- **Classes**: `kebab-case` (e.g., `ticket-dashboard`)
- **IDs**: `kebab-case` (e.g., `main-content`)
- **BEM Notation**: For complex components
  ```css
  .ticket-card {}
  .ticket-card__header {}
  .ticket-card__header--highlighted {}
  ```

---

## Python Style Guide

### Code Formatting

Follow **PEP 8** with the following specifications:

#### Line Length
```python
# Maximum line length: 100 characters (not 79)
# For long strings, use implicit concatenation or parentheses
long_message = (
    "This is a very long message that needs to be split "
    "across multiple lines for readability and compliance."
)
```

#### Indentation
```python
# Use 4 spaces (never tabs)
def process_ticket(ticket_data):
    if ticket_data:
        result = analyze_ticket(
            ticket_data,
            include_history=True,
            depth=2
        )
        return result
```

#### Imports
```python
# Order: standard library, third-party, local
# Alphabetize within each group
# Use absolute imports

# Standard library
import json
import os
from datetime import datetime

# Third-party
from flask import Flask, request
from sqlalchemy import Column, String

# Local
from models import Ticket, User
from utils.validators import validate_email
```

#### Whitespace
```python
# Two blank lines before top-level functions/classes
# One blank line between methods


class TicketProcessor:
    """Process incoming tickets."""

    def __init__(self, client):
        self.client = client

    def process(self, data):
        return self._analyze(data)


def standalone_function():
    """Standalone function."""
    pass
```

### Docstrings

Use **Google Style** docstrings:

```python
def process_ticket(ticket_id, include_history=False):
    """Process a support ticket with AI agents.

    Analyzes the ticket through multiple AI agents including classification,
    diagnosis, and solution generation. Optionally includes historical context
    from similar past tickets.

    Args:
        ticket_id (str): Unique identifier for the ticket (e.g., 'TKT-A4D3106B').
        include_history (bool, optional): Whether to include historical context.
            Defaults to False.

    Returns:
        dict: Processing results containing:
            - classification (dict): Category, urgency, expertise level
            - diagnosis (dict): Root cause analysis
            - solution (dict): Step-by-step resolution

    Raises:
        ValueError: If ticket_id is invalid or not found.
        DatabaseError: If database connection fails.

    Examples:
        >>> result = process_ticket('TKT-12345', include_history=True)
        >>> print(result['classification']['urgency'])
        'high'

    Note:
        This function makes external API calls to Claude and may take
        several seconds to complete.
    """
    # Implementation
    pass
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import Dict, List, Optional, Union

def fetch_tickets(
    status: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Union[str, int]]]:
    """Fetch tickets from database with optional filtering.

    Args:
        status: Filter by ticket status (open, in_progress, etc.)
        limit: Maximum number of tickets to return

    Returns:
        List of ticket dictionaries
    """
    # Implementation
    pass
```

### Error Handling

```python
# Be specific with exception types
try:
    ticket = db.session.get(Ticket, ticket_id)
    if not ticket:
        raise ValueError(f"Ticket {ticket_id} not found")
except ValueError as e:
    logger.error(f"Validation error: {e}")
    return {"error": str(e)}, 400
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    return {"error": "Database error"}, 500
except Exception as e:
    logger.critical(f"Unexpected error: {e}")
    return {"error": "Internal server error"}, 500
```

### Class Design

```python
class BaseAgent:
    """Base class for all AI agents.

    Provides common functionality for agent initialization, logging,
    and Claude API interaction.

    Attributes:
        client: Anthropic API client instance
        name: Agent identifier for logging
        logger: Logger instance for this agent
    """

    def __init__(self, client: Anthropic, name: str):
        """Initialize the base agent.

        Args:
            client: Anthropic API client
            name: Unique name for this agent
        """
        self.client = client
        self.name = name
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up logger for this agent (private method)."""
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        return logger

    def call_claude(self, messages: List[Dict], system_prompt: str) -> str:
        """Make API call to Claude (public method)."""
        # Implementation
        pass
```

### Constants and Configuration

```python
# Define constants at module level
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
API_VERSION = "v1"

# Use dataclasses for configuration
from dataclasses import dataclass

@dataclass
class AgentConfig:
    """Configuration for AI agents."""
    model: str = "claude-sonnet-4-5"
    max_tokens: int = 4096
    temperature: float = 0.7
```

### SQL and Database

```python
# Use SQLAlchemy ORM, not raw SQL
# Good
tickets = Ticket.query.filter_by(status='open').all()

# Bad - avoid raw SQL
tickets = db.execute("SELECT * FROM tickets WHERE status='open'")

# Use session.get() instead of deprecated Query.get()
# Good
ticket = db.session.get(Ticket, ticket_id)

# Bad - deprecated
ticket = Ticket.query.get(ticket_id)
```

---

## JavaScript/React Style Guide

### Code Formatting

Follow **Airbnb JavaScript Style Guide** with React extensions:

#### General Rules

```javascript
// Use 2 spaces for indentation
// Use single quotes for strings
// Always use semicolons
// Use const/let, never var

const processTicket = (ticketData) => {
  const { subject, description } = ticketData;
  return {
    id: generateId(),
    subject,
    description,
    createdAt: new Date().toISOString()
  };
};
```

#### React Components

```javascript
// Functional components with hooks (preferred)
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const TicketDashboard = ({ tickets, onSelectTicket }) => {
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Side effects here
    return () => {
      // Cleanup here
    };
  }, []);

  const handleFilterChange = (newFilter) => {
    setFilter(newFilter);
  };

  return (
    <div className="ticket-dashboard">
      {/* Component JSX */}
    </div>
  );
};

// PropTypes for type checking
TicketDashboard.propTypes = {
  tickets: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string.isRequired,
    subject: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired
  })).isRequired,
  onSelectTicket: PropTypes.func.isRequired
};

// Default props
TicketDashboard.defaultProps = {
  tickets: []
};

export default TicketDashboard;
```

#### Component Organization

```javascript
// 1. Imports
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import './TicketCard.css';

// 2. Helper functions (outside component)
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};

// 3. Component
const TicketCard = ({ ticket, onClick }) => {
  // 3a. Hooks
  const [isExpanded, setIsExpanded] = useState(false);

  // 3b. Event handlers
  const handleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  // 3c. Computed values
  const displayDate = formatDate(ticket.createdAt);

  // 3d. Render
  return (
    <div className="ticket-card" onClick={onClick}>
      {/* JSX */}
    </div>
  );
};

// 4. PropTypes
TicketCard.propTypes = {
  ticket: PropTypes.object.isRequired,
  onClick: PropTypes.func
};

// 5. Export
export default TicketCard;
```

#### Destructuring

```javascript
// Destructure props and state
// Good
const TicketDetail = ({ ticket, onClose }) => {
  const { id, subject, description, status } = ticket;
  return <div>{subject}</div>;
};

// Bad
const TicketDetail = (props) => {
  return <div>{props.ticket.subject}</div>;
};
```

#### Event Handlers

```javascript
// Name handlers with 'handle' prefix
const handleSubmit = (event) => {
  event.preventDefault();
  // Handle submission
};

const handleInputChange = (event) => {
  const { name, value } = event.target;
  setFormData({ ...formData, [name]: value });
};
```

#### Conditional Rendering

```javascript
// Use short-circuit evaluation for simple conditions
{isLoading && <LoadingSpinner />}

// Use ternary for if/else
{tickets.length > 0 ? (
  <TicketList tickets={tickets} />
) : (
  <EmptyState message="No tickets found" />
)}

// Extract complex conditions to variables
const shouldShowDetails = ticket && ticket.status === 'open';
{shouldShowDetails && <TicketDetails ticket={ticket} />}
```

#### Async Operations

```javascript
// Use async/await with try/catch
const fetchTickets = async () => {
  setLoading(true);
  try {
    const response = await fetch('http://localhost:5000/api/tickets');
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    const data = await response.json();
    setTickets(data);
  } catch (error) {
    console.error('Error fetching tickets:', error);
    setError(error.message);
  } finally {
    setLoading(false);
  }
};
```

#### Comments and JSDoc

```javascript
/**
 * Fetches tickets from the API and updates component state
 *
 * @param {string} status - Filter tickets by status (optional)
 * @returns {Promise<void>}
 * @throws {Error} If API request fails
 */
const fetchTickets = async (status = null) => {
  // Implementation
};

// Inline comments for complex logic
// Calculate the urgency score based on multiple factors
const urgencyScore = (
  ticket.priority * 2 +
  ticket.age * 0.5 +
  ticket.customerTier * 1.5
);
```

---

## CSS Style Guide

### General Principles

```css
/* Use mobile-first responsive design */
/* Organize properties alphabetically */
/* Use CSS custom properties for theming */
/* Avoid !important unless absolutely necessary */
```

### CSS Organization

```css
/* 1. CSS Variables */
:root {
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  --color-success: #10b981;
  --color-danger: #ef4444;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;
  --border-radius: 8px;
  --transition-speed: 0.2s;
}

/* 2. Reset/Base Styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* 3. Typography */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 16px;
  line-height: 1.5;
}

/* 4. Layout */
.container {
  margin: 0 auto;
  max-width: 1200px;
  padding: var(--spacing-md);
}

/* 5. Components */
.ticket-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: var(--border-radius);
  padding: var(--spacing-md);
  transition: all var(--transition-speed);
}

/* 6. States */
.ticket-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.ticket-card.is-selected {
  border-color: var(--color-primary);
}

/* 7. Media Queries (mobile-first) */
@media (min-width: 768px) {
  .ticket-card {
    padding: var(--spacing-lg);
  }
}
```

### Naming Conventions

```css
/* Use BEM (Block Element Modifier) for complex components */

/* Block */
.ticket-dashboard {}

/* Element */
.ticket-dashboard__header {}
.ticket-dashboard__content {}

/* Modifier */
.ticket-dashboard--loading {}
.ticket-dashboard__header--sticky {}

/* State classes */
.is-active {}
.is-disabled {}
.is-loading {}
.has-error {}
```

### Property Ordering

```css
.selector {
  /* Positioning */
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 10;

  /* Display & Box Model */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100vh;
  margin: 1rem;
  padding: 1rem;
  border: 1px solid #000;
  border-radius: 4px;

  /* Typography */
  color: #333;
  font-family: Arial, sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  text-align: center;

  /* Visual */
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  opacity: 1;

  /* Animation */
  transition: all 0.3s ease;
  transform: translateX(0);

  /* Misc */
  cursor: pointer;
  overflow: hidden;
}
```

### Responsive Design

```css
/* Mobile-first approach */

/* Base styles (mobile) */
.ticket-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
}

/* Tablet */
@media (min-width: 768px) {
  .ticket-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .ticket-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Large Desktop */
@media (min-width: 1440px) {
  .ticket-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

---

## Git Conventions

### Commit Messages

Follow **Conventional Commits** specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build, etc.)
- `ci`: CI/CD changes
- `revert`: Revert previous commit

#### Examples

```bash
# Feature
feat(dashboard): add specialist assignment visibility to ticket cards

# Bug fix
fix(api): resolve SQLAlchemy deprecation warnings in ticket queries

# Documentation
docs(readme): add deployment section with Docker configuration

# Multiple paragraphs
feat(agents): implement new escalation agent for complex tickets

This agent handles tickets that require human intervention by:
- Analyzing confidence scores from solution agent
- Checking historical escalation patterns
- Routing to appropriate tier-2 specialists

Closes #123
```

#### Rules

1. **Subject Line**
   - Use imperative mood ("add" not "added" or "adds")
   - No period at the end
   - Maximum 72 characters
   - Lowercase after type

2. **Body** (optional)
   - Wrap at 72 characters
   - Explain what and why, not how
   - Separate from subject with blank line

3. **Footer** (optional)
   - Reference issues: `Closes #123`, `Fixes #456`
   - Breaking changes: `BREAKING CHANGE: description`

### Branch Naming

```bash
# Format: type/short-description

# Features
feature/ticket-filtering
feature/user-authentication

# Bug fixes
fix/dashboard-loading-error
fix/assignment-null-check

# Hotfixes
hotfix/critical-api-error

# Releases
release/v1.2.0

# Examples
git checkout -b feature/add-export-functionality
git checkout -b fix/resolve-redis-connection-timeout
```

### Pull Request Guidelines

#### Title Format
```
[TYPE] Short description of changes
```

#### Description Template
```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Changes Made
- Detailed list of changes
- One item per significant change
- Be specific

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- Describe test scenarios

## Screenshots (if applicable)
Add screenshots for UI changes

## Related Issues
Closes #123
Relates to #456

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added to complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests passing
```

---

## Documentation Standards

### Code Comments

```python
# Good comments explain WHY, not WHAT

# Bad - states the obvious
# Increment counter by 1
counter += 1

# Good - explains reasoning
# Increment counter to track retry attempts for rate limiting
counter += 1

# Bad - redundant
# Get the user's email address
email = user.email

# Good - explains business logic
# Use primary email for notifications, fallback to secondary if primary is invalid
email = user.primary_email or user.secondary_email
```

### Function Documentation

```python
def assign_specialist(ticket: Dict, specialists: List[User]) -> Optional[User]:
    """Assign the most appropriate specialist to a ticket.

    Uses a scoring algorithm based on:
    - Specialist expertise match with ticket category
    - Current workload (number of active tickets)
    - Historical resolution success rate
    - Availability status

    Args:
        ticket: Ticket data including category and urgency
        specialists: List of available specialist users

    Returns:
        Best matching specialist, or None if no match found

    Raises:
        ValueError: If ticket missing required fields

    Example:
        >>> ticket = {'category': 'network', 'urgency': 'high'}
        >>> specialist = assign_specialist(ticket, available_specialists)
        >>> print(specialist.name)
        'John Smith'

    Note:
        This function has O(n) complexity where n is number of specialists.
        For large specialist pools, consider implementing caching.
    """
    # Implementation
```

### README Structure

Every module should have a README explaining:

1. **Purpose**: What does this module do?
2. **Usage**: How to use it (with examples)
3. **Dependencies**: What does it require?
4. **Configuration**: Any setup needed
5. **API**: Public functions/classes
6. **Examples**: Real-world usage examples

### Inline Documentation

```javascript
/**
 * Ticket Dashboard Component
 *
 * Displays a grid of ticket cards with filtering and sorting capabilities.
 * Supports real-time updates via WebSocket connection.
 *
 * @component
 * @example
 * <TicketDashboard
 *   tickets={ticketList}
 *   onSelectTicket={handleSelection}
 *   filter="open"
 * />
 */
const TicketDashboard = ({ tickets, onSelectTicket, filter }) => {
  // Component implementation
};
```

---

## API Design Principles

### RESTful Conventions

```python
# Resource naming
GET    /api/tickets              # List all tickets
POST   /api/tickets              # Create new ticket
GET    /api/tickets/:id          # Get specific ticket
PUT    /api/tickets/:id          # Update ticket (full)
PATCH  /api/tickets/:id          # Update ticket (partial)
DELETE /api/tickets/:id          # Delete ticket

# Nested resources
GET    /api/tickets/:id/assignments    # Get ticket assignments
POST   /api/tickets/:id/assignments    # Assign to ticket

# Filtering, sorting, pagination
GET    /api/tickets?status=open&sort=created_at&limit=20&offset=0
```

### Request/Response Format

```python
# Request - use JSON
POST /api/tickets
Content-Type: application/json

{
  "user_email": "user@example.com",
  "subject": "Issue description",
  "description": "Detailed information"
}

# Response - consistent structure
{
  "success": true,
  "data": {
    "ticket_id": "TKT-12345",
    "status": "open"
  },
  "metadata": {
    "timestamp": "2025-12-22T14:48:41Z",
    "version": "1.0"
  }
}

# Error response - consistent structure
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "user_email",
      "value": "invalid-email"
    }
  },
  "metadata": {
    "timestamp": "2025-12-22T14:48:41Z",
    "request_id": "req-abc123"
  }
}
```

### HTTP Status Codes

```python
# Success
200 OK                  # Successful GET, PUT, PATCH
201 Created            # Successful POST
204 No Content         # Successful DELETE

# Client Errors
400 Bad Request        # Invalid request data
401 Unauthorized       # Authentication required
403 Forbidden          # Insufficient permissions
404 Not Found          # Resource doesn't exist
409 Conflict           # Resource conflict (duplicate)
422 Unprocessable      # Validation errors

# Server Errors
500 Internal Error     # Server error
502 Bad Gateway        # Upstream service error
503 Service Unavailable # Temporary unavailability
```

### Versioning

```python
# Version in URL (preferred for major changes)
/api/v1/tickets
/api/v2/tickets

# Version in header (for minor changes)
GET /api/tickets
Accept: application/vnd.ithelper.v1+json
```

---

## Database Conventions

### Table Naming

```sql
-- Use plural nouns
tickets
users
classifications
ticket_assignments

-- Use snake_case
workflow_logs
user_preferences
```

### Column Naming

```sql
-- Use snake_case
user_id
created_at
email_address

-- Boolean columns - use is/has prefix
is_active
has_attachment
is_deleted

-- Foreign keys - use singular_table_id
ticket_id  -- references tickets(id)
user_id    -- references users(id)
```

### Indexes

```python
# Add indexes for:
# - Foreign keys
# - Frequently queried columns
# - Columns in WHERE clauses
# - Columns in ORDER BY clauses

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.String, primary_key=True)
    user_email = db.Column(db.String, index=True)  # Frequently queried
    status = db.Column(db.Enum(TicketStatus), index=True)  # Used in filters
    created_at = db.Column(db.DateTime, index=True)  # Used for sorting
```

### Migrations

```python
# Always use migrations for schema changes
# Never modify database directly

# Create migration
alembic revision -m "Add urgency column to tickets"

# Migration file
def upgrade():
    op.add_column('tickets',
        sa.Column('urgency', sa.String(20), nullable=True)
    )

def downgrade():
    op.drop_column('tickets', 'urgency')
```

---

## Testing Standards

### Test Organization

```python
# tests/test_ticket_api.py

import pytest
from app import app, db
from models import Ticket

class TestTicketAPI:
    """Test suite for ticket API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def sample_ticket(self):
        """Create sample ticket data."""
        return {
            "user_email": "test@example.com",
            "subject": "Test ticket",
            "description": "Test description"
        }

    def test_create_ticket_success(self, client, sample_ticket):
        """Test successful ticket creation."""
        response = client.post('/api/tickets', json=sample_ticket)

        assert response.status_code == 201
        assert response.json['success'] is True
        assert 'ticket_id' in response.json

    def test_create_ticket_missing_email(self, client, sample_ticket):
        """Test ticket creation fails without email."""
        del sample_ticket['user_email']
        response = client.post('/api/tickets', json=sample_ticket)

        assert response.status_code == 400
        assert 'error' in response.json
```

### Test Naming

```python
# Format: test_<function>_<scenario>_<expected>

def test_process_ticket_valid_input_returns_result():
    """Test that valid ticket input returns processing result."""
    pass

def test_assign_specialist_no_match_returns_none():
    """Test that no specialist match returns None."""
    pass

def test_fetch_tickets_invalid_status_raises_error():
    """Test that invalid status raises ValueError."""
    pass
```

### Coverage Requirements

- **Minimum coverage**: 80% overall
- **Critical paths**: 100% coverage
- **New code**: Must not decrease overall coverage
- **Run coverage**: `pytest --cov=src --cov-report=html`

### Testing Best Practices

```python
# 1. AAA Pattern: Arrange, Act, Assert
def test_ticket_status_update():
    # Arrange
    ticket = Ticket(id='TKT-123', status='open')

    # Act
    ticket.status = 'in_progress'

    # Assert
    assert ticket.status == 'in_progress'

# 2. One assertion per test (when possible)
def test_ticket_has_id():
    ticket = create_ticket()
    assert ticket.id is not None

def test_ticket_has_timestamp():
    ticket = create_ticket()
    assert ticket.created_at is not None

# 3. Use fixtures for common setup
@pytest.fixture
def authenticated_client():
    client = app.test_client()
    client.post('/login', json={'email': 'test@example.com'})
    return client

# 4. Test edge cases
def test_assign_specialist_empty_list_returns_none():
    result = assign_specialist(ticket, [])
    assert result is None

def test_assign_specialist_none_list_raises_error():
    with pytest.raises(TypeError):
        assign_specialist(ticket, None)
```

---

## Security Best Practices

### Input Validation

```python
from flask import request
from marshmallow import Schema, fields, ValidationError

class TicketSchema(Schema):
    """Validate ticket input."""
    user_email = fields.Email(required=True)
    subject = fields.Str(required=True, validate=lambda s: 5 <= len(s) <= 200)
    description = fields.Str(required=True, validate=lambda s: 10 <= len(s) <= 5000)

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    schema = TicketSchema()

    try:
        # Validate input
        data = schema.load(request.get_json())
    except ValidationError as e:
        return {"error": "Invalid input", "details": e.messages}, 400

    # Process valid data
    ticket = process_ticket(data)
    return {"ticket_id": ticket.id}, 201
```

### SQL Injection Prevention

```python
# Always use ORM or parameterized queries

# Good - using ORM
tickets = Ticket.query.filter_by(user_email=email).all()

# Good - parameterized query
tickets = db.execute(
    "SELECT * FROM tickets WHERE user_email = :email",
    {"email": email}
).fetchall()

# BAD - vulnerable to SQL injection
tickets = db.execute(
    f"SELECT * FROM tickets WHERE user_email = '{email}'"
).fetchall()
```

### Authentication & Authorization

```python
from functools import wraps
from flask import request, g

def require_auth(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return {"error": "Authentication required"}, 401

        user = validate_token(token)
        if not user:
            return {"error": "Invalid token"}, 401

        g.current_user = user
        return f(*args, **kwargs)

    return decorated_function

@app.route('/api/tickets', methods=['POST'])
@require_auth
def create_ticket():
    # Only authenticated users can create tickets
    pass
```

### Sensitive Data

```python
# Never log sensitive data
import logging

# Bad
logger.info(f"User logged in: {user.email} with password {password}")

# Good
logger.info(f"User logged in: {user.email}")

# Never commit secrets to git
# Use environment variables
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Add to .gitignore
.env
secrets.json
*.pem
*.key
```

### CORS Configuration

```python
from flask_cors import CORS

# Production - be specific
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Development only
CORS(app)  # Allow all origins
```

---

## Code Review Guidelines

### Reviewer Responsibilities

1. **Functionality**
   - Does the code work as intended?
   - Are edge cases handled?
   - Are there potential bugs?

2. **Design**
   - Is the code well-designed?
   - Does it fit the architecture?
   - Is it the right abstraction level?

3. **Complexity**
   - Is the code easy to understand?
   - Can it be simplified?
   - Is it over-engineered?

4. **Tests**
   - Are there adequate tests?
   - Do tests cover edge cases?
   - Are tests meaningful?

5. **Style**
   - Does code follow style guide?
   - Are naming conventions followed?
   - Is formatting consistent?

6. **Documentation**
   - Are complex parts documented?
   - Are docstrings complete?
   - Is the README updated?

### Review Checklist

```markdown
## Code Review Checklist

### Functionality
- [ ] Code accomplishes intended purpose
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No obvious bugs

### Design
- [ ] Follows SOLID principles
- [ ] Appropriate abstractions
- [ ] No code duplication
- [ ] Consistent with existing patterns

### Testing
- [ ] Unit tests added/updated
- [ ] Tests are meaningful
- [ ] Edge cases tested
- [ ] Coverage maintained/improved

### Security
- [ ] Input validation present
- [ ] No SQL injection vulnerabilities
- [ ] No sensitive data in logs
- [ ] Authentication/authorization correct

### Performance
- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] No N+1 queries
- [ ] Appropriate caching

### Documentation
- [ ] Complex code commented
- [ ] Docstrings complete
- [ ] README updated if needed
- [ ] API docs updated if needed

### Style
- [ ] Follows style guide
- [ ] Naming conventions followed
- [ ] Formatting consistent
- [ ] No linting errors
```

### Providing Feedback

```markdown
# Good feedback is:

## Specific
❌ "This code is confusing"
✅ "The variable name `data` is too generic. Consider `ticket_data` or `user_input`"

## Actionable
❌ "This could be better"
✅ "Consider extracting this into a separate function for reusability"

## Kind
❌ "This is terrible code"
✅ "This works, but we can improve readability by..."

## Educational
❌ "Wrong approach"
✅ "Consider using list comprehension here for better performance:
    [x for x in items if x.active] instead of filter()"

## Balanced
- Point out good things too
- "Nice use of type hints here"
- "Good test coverage on this feature"
```

---

## Performance Standards

### Backend Performance

```python
# Database query optimization

# Bad - N+1 query problem
tickets = Ticket.query.all()
for ticket in tickets:
    user = User.query.get(ticket.user_id)  # N additional queries
    print(user.name)

# Good - use eager loading
tickets = Ticket.query.options(
    joinedload(Ticket.user)
).all()
for ticket in tickets:
    print(ticket.user.name)  # No additional queries

# Add indexes for frequently queried columns
class Ticket(db.Model):
    user_email = db.Column(db.String, index=True)
    created_at = db.Column(db.DateTime, index=True)
```

### Frontend Performance

```javascript
// Use React.memo for expensive components
const TicketCard = React.memo(({ ticket, onClick }) => {
  return (
    <div onClick={onClick}>
      {ticket.subject}
    </div>
  );
}, (prevProps, nextProps) => {
  // Only re-render if ticket.id changed
  return prevProps.ticket.id === nextProps.ticket.id;
});

// Use useMemo for expensive calculations
const sortedTickets = useMemo(() => {
  return tickets.sort((a, b) =>
    new Date(b.created_at) - new Date(a.created_at)
  );
}, [tickets]);

// Use useCallback for event handlers passed to children
const handleTicketClick = useCallback((ticketId) => {
  setSelectedTicket(ticketId);
}, []);
```

### Performance Budgets

- **API Response Time**: < 200ms (p95)
- **Database Queries**: < 100ms (p95)
- **Page Load Time**: < 2s (First Contentful Paint)
- **Time to Interactive**: < 3s
- **Bundle Size**: < 250KB (gzipped)

---

## Accessibility Standards

### WCAG 2.1 Level AA Compliance

```jsx
// Semantic HTML
// Bad
<div onClick={handleClick}>Submit</div>

// Good
<button onClick={handleClick}>Submit</button>

// ARIA labels for screen readers
<button
  aria-label="Close ticket detail modal"
  onClick={handleClose}
>
  ×
</button>

// Alt text for images
<img
  src="/specialist-avatar.jpg"
  alt="Profile photo of John Smith, Network Specialist"
/>

// Form labels
<label htmlFor="user-email">
  Email Address
  <input
    id="user-email"
    type="email"
    name="email"
    required
  />
</label>

// Keyboard navigation
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyPress={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
>
  Click me
</div>
```

### Color Contrast

```css
/* Ensure WCAG AA contrast ratios */

/* Minimum contrast: 4.5:1 for normal text */
.text {
  color: #333333;  /* Dark gray */
  background: #ffffff;  /* White - 12.6:1 ratio ✓ */
}

/* Minimum contrast: 3:1 for large text (18pt+) */
.heading {
  color: #666666;  /* Medium gray */
  background: #ffffff;  /* White - 5.7:1 ratio ✓ */
  font-size: 24px;
}

/* Don't rely on color alone */
/* Bad */
.error { color: red; }

/* Good - use icons + text + color */
.error {
  color: #dc2626;
}
.error::before {
  content: "⚠ ";
}
```

### Focus Indicators

```css
/* Never remove focus outlines without replacement */

/* Bad */
button:focus {
  outline: none;
}

/* Good */
button:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

button:focus:not(:focus-visible) {
  outline: none;
}

button:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}
```

---

## Error Handling

### Frontend Error Handling

```javascript
// Error boundaries for React
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Log to error reporting service
    logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-container">
          <h2>Something went wrong</h2>
          <p>We've been notified and are working on it.</p>
          <button onClick={() => window.location.reload()}>
            Reload Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Async error handling
const fetchTickets = async () => {
  try {
    setLoading(true);
    setError(null);

    const response = await fetch('/api/tickets');

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    setTickets(data);

  } catch (error) {
    console.error('Failed to fetch tickets:', error);
    setError('Unable to load tickets. Please try again.');

    // Log to monitoring service
    logError(error, { context: 'fetchTickets' });

  } finally {
    setLoading(false);
  }
};
```

### Backend Error Handling

```python
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def handle_errors(f):
    """Decorator for consistent error handling."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error in {f.__name__}: {e}")
            return {"error": str(e)}, 400
        except DatabaseError as e:
            logger.error(f"Database error in {f.__name__}: {e}")
            return {"error": "Database error occurred"}, 500
        except Exception as e:
            logger.exception(f"Unexpected error in {f.__name__}: {e}")
            return {"error": "Internal server error"}, 500

    return decorated_function

@app.route('/api/tickets', methods=['POST'])
@handle_errors
def create_ticket():
    data = request.get_json()

    # Validation
    if not data.get('user_email'):
        raise ValueError("Email is required")

    # Process
    ticket = process_ticket(data)
    return {"ticket_id": ticket.id}, 201
```

---

## Enforcement and Tools

### Linting

```bash
# Python - Flake8
flake8 src/ --max-line-length=100 --exclude=venv

# Python - Black (formatter)
black src/ --line-length=100

# Python - isort (import sorting)
isort src/

# JavaScript - ESLint
eslint src/ --ext .js,.jsx

# JavaScript - Prettier (formatter)
prettier --write "src/**/*.{js,jsx,css}"
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100]

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.44.0
    hooks:
      - id: eslint
        files: \.(js|jsx)$
```

### CI/CD Integration

```yaml
# .github/workflows/quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  python-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install flake8 black pytest pytest-cov
      - name: Lint with flake8
        run: flake8 src/
      - name: Check formatting with black
        run: black --check src/
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  javascript-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: cd src/frontend && npm ci
      - name: Lint
        run: cd src/frontend && npm run lint
      - name: Test
        run: cd src/frontend && npm test
```

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-22 | Engineering Team | Initial release |

---

## Questions or Suggestions

For questions about this style guide or to suggest improvements:

- **Email**: engineering@yourcompany.com
- **Slack**: #engineering-standards
- **GitHub**: Open an issue with the `style-guide` label

---

**This style guide is a living document and will be updated as our practices evolve.**

*Maintained by the IT Helper Engineering Team*
