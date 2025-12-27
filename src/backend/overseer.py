import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mas_agents.intake_agent import IntakeAgent
from mas_agents.classifier_agent import ClassifierAgent
from mas_agents.diagnostic_agent import DiagnosticAgent
from mas_agents.fetch_agent import FetchAgent
from mas_agents.solution_agent import SolutionAgent
from assignment import assign_ticket


# Overseer class to manage the workflow
class Overseer:
    def __init__(self, client, redis_client):
        self.intake_agent = IntakeAgent(client)
        self.classifier_agent = ClassifierAgent(client)
        self.diagnostic_agent = DiagnosticAgent(client)
        self.fetch_agent = FetchAgent(redis_client)
        self.solution_agent = SolutionAgent(client)
    
    def process_ticket(self, raw_ticket):
        workflow_log = []
        
        # Step 1: Intake
        intake_result = self.intake_agent.process(raw_ticket)
        if not intake_result:
            return {"error": "Intake processing failed", "workflow_log": workflow_log}
        workflow_log.append("IntakeAgent: Successfully processed")
        
        # Step 2: Classify
        classification_result = self.classifier_agent.process(intake_result)
        if not classification_result:
            return {"error": "Classification failed", "workflow_log": workflow_log}
        workflow_log.append(f"ClassifierAgent: Classified as {classification_result['category']} - {classification_result['urgency']}")
        
        assignments = assign_ticket(intake_result, classification_result)
        if not assignments or assignments is None:
            print("No assignments returned from assign_ticket")
            assignments = {'primary': None, 'secondary': None}
            workflow_log.append("AssignmentService: Assignment failed - no users found")
        else:
            print("Assignments:", assignments)
            primary_name = assignments.get('primary', {}).get('name', 'None') if assignments.get('primary') else 'None'
            secondary_name = assignments.get('secondary', {}).get('name', 'None') if assignments.get('secondary') else 'None'
        workflow_log.append(f"AssignmentService: Primary={primary_name}, Secondary={secondary_name}")
        diagnostic_result = self.diagnostic_agent.process(classification_result)
        if not diagnostic_result:
            return {"error": "Diagnostic failed", "workflow_log": workflow_log}
        workflow_log.append("DiagnosticAgent: Diagnosis completed")
        
        # Step 4: Fetch similar solutions
        fetch_query = {"category": classification_result.get('category')}
        fetch_result = self.fetch_agent.process(fetch_query)
        if not fetch_result:
            return {"error": "Fetch similar resolutions failed", "workflow_log": workflow_log}
        workflow_log.append(f"FetchAgent: Found {len(fetch_result.get('past_solutions', []))} similar tickets")
        
        # Step 5: Generate solution
        solution_result = self.solution_agent.process(diagnostic_result, fetch_result)
        if not solution_result:
            return {"error": "Solution generation failed", "workflow_log": workflow_log}    
        workflow_log.append("SolutionAgent: Generated solution")
        
        # Return combined result
        return {
            "intake_result": intake_result,
            "classification": classification_result,
            "assignments": assignments,
            "diagnosis": diagnostic_result,
            "fetched_data": fetch_result,
            "solution": solution_result,
            "workflow_log": workflow_log,
            "status": "solution_generated"
        }