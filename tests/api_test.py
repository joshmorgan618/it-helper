import requests

# Create ticket
response = requests.post('http://127.0.0.1:5000/api/tickets', json={
    "user_email": "test@company.com",
    "subject": "Printer not working",
    "description": "Cannot connect to network printer"
})

print(response.json())
ticket_id = response.json()['ticket_id']

# Get ticket
response = requests.get(f'http://127.0.0.1:5000/api/tickets/{ticket_id}')
print(response.json())