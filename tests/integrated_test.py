import requests
import json
import time

# Base URL for your Flask API
BASE_URL = "http://127.0.0.1:5000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_create_ticket():
    """Test creating a ticket through the full overseer pipeline"""
    print_section("TEST 1: Create Ticket with Overseer Processing")
    
    # Sample ticket data
    ticket_data = {
        "user_email": "john.doe@company.com",
        "subject": "printer broken on 3rd floor!!!",
        "description": "cant print anything, need this fixed asap for my meeting in 1 hour"
    }
    
    print("📤 Sending ticket:")
    print(json.dumps(ticket_data, indent=2))
    print("\n⏳ Processing through overseer (this may take 10-20 seconds)...\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/tickets",
            json=ticket_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ SUCCESS!")
            print("\n📋 Response:")
            print(json.dumps(result, indent=2))
            return result.get('ticket_id')
        else:
            print("❌ FAILED!")
            print(response.json())
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to Flask server.")
        print("Make sure your Flask app is running on http://127.0.0.1:5000")
        return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

def test_get_ticket(ticket_id):
    """Test retrieving a ticket with all related data"""
    if not ticket_id:
        print("⚠️  Skipping GET test - no ticket ID available")
        return
    
    print_section(f"TEST 2: Retrieve Ticket Details - {ticket_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/tickets/{ticket_id}")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print("\n📋 Full Ticket Details:")
            print(json.dumps(result, indent=2))
            
            # Print summary
            print("\n📊 Summary:")
            print(f"  Subject: {result.get('subject')}")
            print(f"  Status: {result.get('status')}")
            if result.get('classification'):
                print(f"  Category: {result['classification'].get('category')}")
                print(f"  Urgency: {result['classification'].get('urgency')}")
            if result.get('solution'):
                print(f"  Estimated Time: {result['solution'].get('estimated_time')}")
                print(f"  Confidence: {result['solution'].get('confidence')}")
                
        else:
            print("❌ FAILED!")
            print(response.json())
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_invalid_input():
    """Test error handling with invalid input"""
    print_section("TEST 3: Invalid Input Handling")
    
    # Missing required field
    invalid_data = {
        "user_email": "test@company.com",
        "subject": "Missing description"
        # description is missing
    }
    
    print("📤 Sending invalid ticket (missing description):")
    print(json.dumps(invalid_data, indent=2))
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/tickets",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ Correctly rejected invalid input!")
            print(response.json())
        else:
            print("⚠️  Unexpected response")
            print(response.json())
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_get_nonexistent_ticket():
    """Test retrieving a ticket that doesn't exist"""
    print_section("TEST 4: Non-existent Ticket Handling")
    
    fake_id = "TKT-FAKE1234"
    print(f"📤 Requesting non-existent ticket: {fake_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/tickets/{fake_id}")
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ Correctly returned 404!")
            print(response.json())
        else:
            print("⚠️  Unexpected response")
            print(response.json())
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_multiple_tickets():
    """Test creating multiple tickets to verify system handles various scenarios"""
    print_section("TEST 5: Multiple Ticket Scenarios")
    
    test_cases = [
        {
            "name": "Software Issue",
            "data": {
                "user_email": "jane@company.com",
                "subject": "excel keeps crashing",
                "description": "every time i open excel it crashes immediately"
            }
        },
        {
            "name": "Network Issue",
            "data": {
                "user_email": "bob@company.com",
                "subject": "wifi not working",
                "description": "cant connect to wifi on 2nd floor, says incorrect password but im using right one"
            }
        },
        {
            "name": "Access Issue",
            "data": {
                "user_email": "alice@company.com",
                "subject": "need access to shared drive",
                "description": "i need access to the finance shared drive for q4 reports"
            }
        }
    ]
    
    created_tickets = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_case['name']} ---")
        print(f"Description: {test_case['data']['description']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/tickets",
                json=test_case['data'],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                result = response.json()
                created_tickets.append(result['ticket_id'])
                print(f"✅ Created: {result['ticket_id']}")
                print(f"   Category: {result['summary'].get('category')}")
                print(f"   Urgency: {result['summary'].get('urgency')}")
            else:
                print(f"❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        # Small delay between requests
        time.sleep(2)
    
    print(f"\n📊 Summary: Created {len(created_tickets)} tickets")
    return created_tickets

def main():
    """Run all tests"""
    print_section("🚀 STARTING INTEGRATED API TESTS")
    print("Testing Flask API with full Overseer integration")
    print("Make sure Flask server is running: python src/backend/app.py")
    input("\nPress Enter to continue...")
    
    # Test 1: Create a ticket
    ticket_id = test_create_ticket()
    
    # Wait a moment for database to finish
    time.sleep(1)
    
    # Test 2: Retrieve the ticket
    test_get_ticket(ticket_id)
    
    # Test 3: Invalid input
    test_invalid_input()
    
    # Test 4: Non-existent ticket
    test_get_nonexistent_ticket()
    
    # Test 5: Multiple scenarios
    test_multiple_tickets()
    
    print_section("✅ ALL TESTS COMPLETED")
    print("Check your PostgreSQL database to verify data was saved correctly:")
    print("  psql it_support_db")
    print("  SELECT * FROM tickets;")
    print("  SELECT * FROM classifications;")
    print("  SELECT * FROM solutions;")

if __name__ == "__main__":
    main()