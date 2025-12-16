# it-helper
For the little things


Gameplay Loop:
 - User submits ticket (input)
      - User says problem (ex. printer not connecting) on React App
      - Frontend sends to Flask API 
- Overseer Agent makes each agent do their job one at a time
- Intake Agent - Makes the input clean into different sections:
    - Email / User
    - Problem
    - Urgency
- Classifier Agent - Reads Structrues Ticket and classifies it into specific groups
- Diangostic Agent - Looks at classification - Searches Redis Memory (have we seen problem before) - Finds Similar Tickets - 
- Retrival Agent - Takes category + diagnostic, searches ChromaDB vector databse for relevant docs - Finds: "printer_network_troubelshooting.md" and "ip_conflict_resolution.md" 
- Solution Agent - Combines diagnosis + past solutions + documentation, generates step by step fix. 
- Audit Logger Agent - Records everything that has happened - Stores to PostgreSQL


**Integrations:**
- Solution Agent checks BEFORE finalizing solution
- If escalation needed → Ticket goes to "Awaiting Approval" status
- Human reviews in Dashboard → Approves or Rejects

---

## **3. HOW SYSTEMS TALK TO EACH OTHER**

### **Data Flow Example: Complete Ticket Processing**
```
1. USER SUBMITS TICKET
   ↓
2. React Dashboard → Flask API
   ↓
3. Flask → WorkflowOrchestrator
   ↓
4. Orchestrator → IntakeAgent → Claude API
   ← IntakeAgent returns structured data
   ↓
5. Orchestrator → ClassifierAgent → Claude API
   ← ClassifierAgent returns category + priority
   ↓
6. Orchestrator → DiagnosticAgent → Redis (search similar)
   ← Redis returns past tickets
   DiagnosticAgent → Claude API (analyze)
   ← Returns root cause analysis
   ↓
7. Orchestrator → KnowledgeRetrievalAgent → ChromaDB (vector search)
   ← Returns relevant documentation
   ↓
8. Orchestrator → SolutionAgent
   SolutionAgent → Claude API (generate solution)
   SolutionAgent → GuardrailSystem (safety check)
   ← GuardrailSystem returns APPROVED or ESCALATE
   ↓
9. If APPROVED:
   Orchestrator → AuditLoggerAgent → PostgreSQL (store log)
   Orchestrator → Redis (store resolution for learning)
   Orchestrator → Flask API → Dashboard (display solution)
   
10. If ESCALATE:
   Orchestrator → PostgreSQL (update status)
   Orchestrator → Flask API → Dashboard (flag for human)
```
