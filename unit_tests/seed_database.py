import csv
from datetime import datetime
import os
import sys
from pathlib import Path

# This is a test script to creates a test database filled with test data 
# to test the database's functions on it

# Add the parent directory to the Python path so we can import the database module
sys.path.append(str(Path(__file__).parent.parent))

from database import DatabaseManager
from classes import Provider, Member, Service, ServiceRecord, Status

def load_csv(filename):
    """Load data from a CSV file"""
    data_dir = "./unit_tests/test_data/"
    with open(f"{data_dir}{filename}", 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def seed_database(db_path='chocan.db'):
    """Seed the database with test data"""
    # Create new database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    db = DatabaseManager(db_path)
    db.create_tables()

    # load and insert providers
    providers = {}  # store providers for later
    for row in load_csv('providers.csv'):
        provider = Provider(
            providerNumber=row['provider_number'],
            firstName=row['first_name'],
            lastName=row['last_name'],
            streetAddress=row['street_address'],
            city=row['city'],
            state=row['state'],
            zipCode=row['zipcode']
        )
        providers[provider._providerNumber] = provider
        db.insert_provider(provider)
    print("Providers loaded successfully")

    # Load and insert members
    members = {}  # Store members for later use
    for row in load_csv('members.csv'):
        member = Member(
            memberNumber=row['member_number'],
            firstName=row['first_name'],
            lastName=row['last_name'],
            streetAddress=row['street_address'],
            city=row['city'],
            state=row['state'],
            zipCode=row['zipcode'],
            status=Status[row['status']]
        )
        members[member._memberNumber] = member
        db.insert_member(member)
    print("Members loaded successfully")

    # Load and insert services
    services = {}  # Store services for later use
    for row in load_csv('services.csv'):
        service = Service(
            serviceCode=row['service_code'],
            serviceName=row['service_name'],
            fee=float(row['fee'])
        )
        services[service._serviceCode] = service
        db.insert_service(service)
    print("Services loaded successfully")

    # Load and insert service records
    for row in load_csv('service_records.csv'):
        service_record = ServiceRecord(
            dateReceived=datetime.fromisoformat(row['date_received']),
            serviceDate=datetime.fromisoformat(row['service_date']).date(),
            provider=providers[row['provider_number']],
            member=members[row['member_number']],
            service=services[row['service_code']],
            comments=row['comments'],
            fee=float(row['fee'])
        )
        db.insert_service_record(service_record)
    print("Service records loaded successfully")

    db.close()
    print(f"\nDatabase seeded successfully at: {db_path}")

if __name__ == "__main__":
    seed_database() 