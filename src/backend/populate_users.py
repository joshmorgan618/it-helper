from app import app
from models import db, User

def populate_users():
    """Populate database with sample IT staff"""
    
    users_data = [
        {
            "email": "john.smith@company.com",
            "name": "John Smith",
            "role": "Phone Specialist",
            "tier_level": "tier2",
            "specialization": "phones",
            "building": "building1"
        },
        {
            "email": "sarah.johnson@company.com",
            "name": "Sarah Johnson",
            "role": "Network Specialist",
            "tier_level": "tier3",
            "specialization": "network",
            "building": None  # Works across all buildings
        },
        {
            "email": "mike.davis@company.com",
            "name": "Mike Davis",
            "role": "General IT Support",
            "tier_level": "tier1",
            "specialization": "general",
            "building": "building2"
        },
        {
            "email": "lisa.chen@company.com",
            "name": "Lisa Chen",
            "role": "Software Specialist",
            "tier_level": "tier2",
            "specialization": "software",
            "building": None  # Department-wide
        },
        {
            "email": "robert.brown@company.com",
            "name": "Robert Brown",
            "role": "General IT Support",
            "tier_level": "tier1",
            "specialization": "general",
            "building": "building1"
        },
        {
            "email": "emma.wilson@company.com",
            "name": "Emma Wilson",
            "role": "Printer Specialist",
            "tier_level": "tier2",
            "specialization": "printers",
            "building": "building3"
        },
        {
            "email": "david.martinez@company.com",
            "name": "David Martinez",
            "role": "Hardware Specialist",
            "tier_level": "tier2",
            "specialization": "hardware",
            "building": None
        },
        {
            "email": "amy.taylor@company.com",
            "name": "Amy Taylor",
            "role": "General IT Support",
            "tier_level": "tier1",
            "specialization": "general",
            "building": "building3"
        }
    ]
    
    with app.app_context():
        # Check if users already exist
        existing_users = User.query.count()
        if existing_users > 0:
            print(f"Database already has {existing_users} users.")
            choice = input("Do you want to add more users anyway? (y/n): ")
            if choice.lower() != 'y':
                print("Aborted.")
                return
        
        # Add all users
        added_count = 0
        for user_data in users_data:
            # Check if email already exists
            existing = User.query.filter_by(email=user_data['email']).first()
            if existing:
                print(f"User {user_data['email']} already exists, skipping...")
                continue
            
            user = User(**user_data)
            db.session.add(user)
            added_count += 1
            print(f"Added: {user_data['name']} ({user_data['specialization']})")
        
        db.session.commit()
        print(f"\nSuccessfully added {added_count} users!")
        print(f"Total users in database: {User.query.count()}")
        
        # Display summary
        print("\n" + "="*60)
        print("IT STAFF SUMMARY")
        print("="*60)
        all_users = User.query.all()
        for user in all_users:
            building = user.building or "All Buildings"
            print(f"{user.name:20} | {user.specialization:12} | {user.tier_level:6} | {building}")
        print("="*60)

if __name__ == "__main__":
    print("Populating IT Support Staff...")
    print()
    populate_users()