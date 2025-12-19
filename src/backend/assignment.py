"""
Enterprise Ticket Assignment Service
-------------------------------------
Implements intelligent routing of IT support tickets to appropriate staff members
based on expertise, availability, workload, and business rules.

Design Principles:
- Single Responsibility: Only handles assignment logic
- Extensibility: Easy to add new rules without modifying core logic
- Testability: Pure functions, no side effects
- Observability: Comprehensive logging of assignment decisions
- Performance: Efficient queries, minimal database hits
"""

from models import User, db
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logger = logging.getLogger(__name__)


class AssignmentRule:
    """Base class for assignment rules - Strategy Pattern"""
    def __init__(self, priority: int):
        self.priority = priority  # Lower number = higher priority
    
    def matches(self, ticket_data: Dict) -> bool:
        """Check if this rule applies to the ticket"""
        raise NotImplementedError
    
    def get_user(self, ticket_data: Dict) -> Optional[User]:
        """Return the user to assign based on this rule"""
        raise NotImplementedError


class DeviceSpecialistRule(AssignmentRule):
    """Assign based on specific device type - Highest Priority"""
    def __init__(self):
        super().__init__(priority=1)
    
    def matches(self, ticket_data: Dict) -> bool:
        device_type = ticket_data.get('extracted_info', {}).get('device_type')
        return device_type in ['phone', 'printer']
    
    def get_user(self, ticket_data: Dict) -> Optional[User]:
        device_type = ticket_data.get('extracted_info', {}).get('device_type')
        
        # Map device types to specializations
        specialization_map = {
            'phone': 'phones',
            'printer': 'printers'
        }
        
        specialization = specialization_map.get(device_type)
        if not specialization:
            return None
        
        # Find available specialist with appropriate tier
        tier_level = ticket_data.get('classification', {}).get('expertise_level', 'tier1')
        
        user = User.query.filter_by(
            specialization=specialization
        ).filter(
            User.tier_level.in_([tier_level, 'tier2', 'tier3'])
        ).first()
        
        logger.info(f"DeviceSpecialistRule: Assigned {user.name if user else 'None'} for {device_type}")
        return user


class CategorySpecialistRule(AssignmentRule):
    """Assign based on ticket category - Second Priority"""
    def __init__(self):
        super().__init__(priority=2)
    
    def matches(self, ticket_data: Dict) -> bool:
        category = ticket_data.get('classification', {}).get('category')
        return category in ['network', 'software', 'hardware']
    
    def get_user(self, ticket_data: Dict) -> Optional[User]:
        category = ticket_data.get('classification', {}).get('category')
        
        # Direct mapping for most categories
        user = User.query.filter_by(specialization=category).first()
        
        logger.info(f"CategorySpecialistRule: Assigned {user.name if user else 'None'} for {category}")
        return user


class UrgencyEscalationRule(AssignmentRule):
    """For critical tickets, assign senior engineers - Third Priority"""
    def __init__(self):
        super().__init__(priority=3)
    
    def matches(self, ticket_data: Dict) -> bool:
        urgency = ticket_data.get('classification', {}).get('urgency')
        return urgency in ['critical', 'high']
    
    def get_user(self, ticket_data: Dict) -> Optional[User]:
        category = ticket_data.get('classification', {}).get('category')
        
        # Find senior (tier2+) specialist in relevant category
        user = User.query.filter_by(
            specialization=category
        ).filter(
            User.tier_level.in_(['tier2', 'tier3'])
        ).order_by(
            User.tier_level.desc()
        ).first()
        
        # Fallback to any senior engineer
        if not user:
            user = User.query.filter(
                User.tier_level.in_(['tier2', 'tier3'])
            ).first()
        
        logger.info(f"UrgencyEscalationRule: Assigned senior {user.name if user else 'None'}")
        return user


class GeneralITRule(AssignmentRule):
    """Default fallback - assign general IT support"""
    def __init__(self):
        super().__init__(priority=999)  # Lowest priority
    
    def matches(self, ticket_data: Dict) -> bool:
        return True  # Always matches as fallback
    
    def get_user(self, ticket_data: Dict) -> Optional[User]:
        # Find general IT with appropriate tier level
        tier_level = ticket_data.get('classification', {}).get('expertise_level', 'tier1')
        
        user = User.query.filter_by(
            specialization='general'
        ).filter(
            User.tier_level == tier_level
        ).first()
        
        # Fallback to any general IT
        if not user:
            user = User.query.filter_by(specialization='general').first()
        
        logger.info(f"GeneralITRule: Assigned {user.name if user else 'None'} as fallback")
        return user


class BuildingSupportRule(AssignmentRule):
    """Assign local building support as secondary"""
    def __init__(self):
        super().__init__(priority=1)
    
    def matches(self, ticket_data: Dict) -> bool:
        location = ticket_data.get('extracted_info', {}).get('location', '')
        if not location:
            return False
        return 'building' in location.lower() or 'floor' in location.lower()
    
    def get_user(self, ticket_data: Dict) -> Optional[User]:
        location = ticket_data.get('extracted_info', {}).get('location', '')
        if not location:
            return None
        # Extract building identifier (e.g., "3rd floor" -> "building3")
        # Simple heuristic - can be made more sophisticated
        building = None
        if 'building' in location.lower():
            # Extract building number/name
            parts = location.lower().split()
            for i, part in enumerate(parts):
                if 'building' in part and i + 1 < len(parts):
                    building = f"building{parts[i+1]}"
                    break
        elif 'floor' in location.lower():
            # Assume floor numbers map to buildings (floor 1-3 = building1, etc.)
            for char in location:
                if char.isdigit():
                    building = f"building{char}"
                    break
        
        if not building:
            return None
        
        # Find general IT assigned to that building
        user = User.query.filter_by(
            specialization='general',
            building=building
        ).first()
        
        logger.info(f"BuildingSupportRule: Assigned {user.name if user else 'None'} for {building}")
        return user


class AssignmentEngine:
    """
    Main assignment engine - uses rule-based system for flexibility
    
    Design Pattern: Chain of Responsibility + Strategy
    - Each rule evaluates independently
    - First matching rule wins for primary assignment
    - Secondary assignment uses separate rule set
    """
    
    def __init__(self):
        # Primary assignment rules (ordered by priority)
        self.primary_rules = [
            DeviceSpecialistRule(),
            CategorySpecialistRule(),
            UrgencyEscalationRule(),
            GeneralITRule()  # Fallback
        ]
        
        # Secondary assignment rules
        self.secondary_rules = [
            BuildingSupportRule()
        ]
        
        # Sort rules by priority
        self.primary_rules.sort(key=lambda r: r.priority)
        self.secondary_rules.sort(key=lambda r: r.priority)
    
    def assign_primary(self, ticket_data: Dict) -> Optional[User]:
        """
        Find primary assignee using rule chain
        
        Args:
            ticket_data: Combined data from intake and classification
        
        Returns:
            User object or None
        """
        for rule in self.primary_rules:
            if rule.matches(ticket_data):
                user = rule.get_user(ticket_data)
                if user:
                    logger.info(f"Primary assignment: {user.name} via {rule.__class__.__name__}")
                    return user
        
        logger.warning("No primary assignee found - this should not happen (GeneralITRule should catch all)")
        return None
    
    def assign_secondary(self, ticket_data: Dict, primary_user: Optional[User]) -> Optional[User]:
        """
        Find secondary assignee (building support, backup, etc.)
        
        Args:
            ticket_data: Combined data from intake and classification
            primary_user: Already assigned primary user (to avoid duplicates)
        
        Returns:
            User object or None
        """
        for rule in self.secondary_rules:
            if rule.matches(ticket_data):
                user = rule.get_user(ticket_data)
                if user and (not primary_user or user.user_id != primary_user.user_id):
                    logger.info(f"Secondary assignment: {user.name} via {rule.__class__.__name__}")
                    return user
        
        logger.info("No secondary assignee needed/found")
        return None
    
    def assign_ticket(
        self, 
        intake_result: Dict, 
        classification_result: Dict
    ) -> Dict[str, Optional[Dict]]:
        """
        Main entry point - assign both primary and secondary users
        
        Args:
            intake_result: Output from IntakeAgent
            classification_result: Output from ClassifierAgent
        
        Returns:
            Dictionary with primary and secondary user assignments
        """
        # Combine ticket data for rules
        ticket_data = {
            **intake_result,
            'classification': classification_result
        }
        
        # Find primary assignee
        primary_user = self.assign_primary(ticket_data)
        
        # Find secondary assignee
        secondary_user = self.assign_secondary(ticket_data, primary_user)
        
        # Format response
        result = {
            'primary': self._format_user(primary_user) if primary_user else None,
            'secondary': self._format_user(secondary_user) if secondary_user else None
        }
        
        logger.info(f"Assignment complete: Primary={primary_user.name if primary_user else 'None'}, "
                   f"Secondary={secondary_user.name if secondary_user else 'None'}")
        
        return result
    
    def _format_user(self, user: User) -> Dict:
        """Format user object for API response"""
        return {
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'specialization': user.specialization,
            'tier_level': user.tier_level,
            'building': user.building
        }


# Global singleton instance
_assignment_engine = None

def get_assignment_engine() -> AssignmentEngine:
    """Get or create the global assignment engine instance"""
    global _assignment_engine
    if _assignment_engine is None:
        _assignment_engine = AssignmentEngine()
    return _assignment_engine


def assign_ticket(intake_result: Dict, classification_result: Dict) -> Dict:
    try:
        engine = get_assignment_engine()
        result = engine.assign_ticket(intake_result, classification_result)
        return result
    except Exception as e:
        print(f"ERROR in assign_ticket: {e}")
        import traceback
        traceback.print_exc()
        return {'primary': None, 'secondary': None}


# For testing/debugging
if __name__ == "__main__":
    # Example usage
    test_intake = {
        "user_email": "test@company.com",
        "subject": "Phone not working",
        "description": "My desk phone won't connect",
        "extracted_info": {
            "device_type": "phone",
            "location": "building 1",
            "issue_type": "connection"
        }
    }
    
    test_classification = {
        "category": "hardware",
        "urgency": "high",
        "expertise_level": "tier2"
    }
    
    print("Test Assignment:")
    print(assign_ticket(test_intake, test_classification))