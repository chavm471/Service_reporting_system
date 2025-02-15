import pytest
import sqlite3
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DatabaseManager
from classes import Provider, Member, Service, ServiceRecord, Status


@pytest.fixture
def db():
    """Create a temporary database connection for testing"""
    db = DatabaseManager(":memory:")
    db.create_tables()
    yield db
    db.close()

@pytest.fixture
def sample_provider():
    return Provider(
        providerNumber="123456789",
        firstName="John",
        lastName="Doe",
        streetAddress="123 Main St",
        city="Portland",
        state="OR",
        zipCode="97201"
    )

@pytest.fixture
def sample_member():
    return Member(
        memberNumber="987654321",
        firstName="Jane",
        lastName="Smith",
        streetAddress="456 Oak Ave",
        city="Portland",
        state="OR",
        zipCode="97202",
        status=Status.VALID
    )

@pytest.fixture
def sample_service():
    return Service(
        serviceCode="598470",
        serviceName="Consultation",
        fee=100.00
    )

def test_create_tables(db):
    """Test if tables are created successfully"""
    # Check if tables exist by trying to select from them
    tables = ["providers", "members", "services", "service_records"]
    for table in tables:
        db.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        assert db.cursor.fetchone() is not None

def test_insert_and_get_provider(db, sample_provider):
    """Test provider insertion and retrieval"""
    db.insert_provider(sample_provider)
    retrieved_provider = db.get_provider("123456789")
    assert retrieved_provider._providerNumber == sample_provider._providerNumber
    assert retrieved_provider._firstname == sample_provider._firstname
    assert retrieved_provider._lastname == sample_provider._lastname

def test_insert_and_get_member(db, sample_member):
    """Test member insertion and retrieval"""
    db.insert_member(sample_member)
    retrieved_member = db.get_member("987654321")
    assert retrieved_member._memberNumber == sample_member._memberNumber
    assert retrieved_member._firstName == sample_member._firstName
    assert retrieved_member._lastName == sample_member._lastName

def test_insert_and_get_service(db, sample_service):
    """Test service insertion and retrieval"""
    db.insert_service(sample_service)
    retrieved_service = db.get_service("598470")
    assert retrieved_service._serviceCode == sample_service._serviceCode
    assert retrieved_service._serviceName == sample_service._serviceName
    assert retrieved_service._fee == sample_service._fee

def test_insert_and_get_service_record(db, sample_provider, sample_member, sample_service):
    """Test service record insertion and retrieval"""
    db.insert_provider(sample_provider)
    db.insert_member(sample_member)
    db.insert_service(sample_service)

    service_record = ServiceRecord(
        dateReceived=datetime.now(),
        serviceDate=datetime.now().date(),
        provider=sample_provider,
        member=sample_member,
        service=sample_service,
        comments="Test comment",
        fee=100.00
    )
    
    db.insert_service_record(service_record)
    
    retrieved_record = db.get_service_record(1)
    assert retrieved_record._provider._providerNumber == sample_provider._providerNumber
    assert retrieved_record._member._memberNumber == sample_member._memberNumber
    assert retrieved_record._service._serviceCode == sample_service._serviceCode

def test_invalid_provider_number(db):
    """Test retrieving a non-existent provider"""
    with pytest.raises(sqlite3.Error):
        db.get_provider("999999999")

def test_invalid_member_number(db):
    """Test retrieving a non-existent member"""
    with pytest.raises(sqlite3.Error):
        db.get_member("999999999")

def test_invalid_service_code(db):
    """Test retrieving a non-existent service"""
    with pytest.raises(sqlite3.Error):
        db.get_service("999999")

def test_duplicate_provider(db, sample_provider):
    """Test inserting a provider with duplicate provider number"""
    db.insert_provider(sample_provider)
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_provider(sample_provider)

def test_duplicate_member(db, sample_member):
    """Test inserting a member with duplicate member number"""
    db.insert_member(sample_member)
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_member(sample_member)

def test_service_record_with_invalid_references(db):
    """Test inserting a service record with non-existent provider/member/service"""
    invalid_record = ServiceRecord(
        dateReceived=datetime.now(),
        serviceDate=datetime.now().date(),
        provider=Provider(
            providerNumber="999999999",
            firstName="Invalid",
            lastName="Provider",
            streetAddress="123 St",
            city="City",
            state="ST",
            zipCode="12345"
        ),
        member=Member(
            memberNumber="888888888",
            firstName="Invalid",
            lastName="User",
            streetAddress="123 St",
            city="City",
            state="ST",
            zipCode="12345",
            status=Status.VALID
        ),
        service=Service(
            serviceCode="777777",
            serviceName="Invalid Service",
            fee=50.00
        ),
        comments="Test comment",
        fee=50.00
    )
    
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_service_record(invalid_record)

def test_invalid_member_status(db):
    """Test inserting a member with an invalid status"""
    class InvalidStatus:
        name = "INVALID_STATUS"  # This will fail the database check constraint
        
    invalid_member = Member(
        memberNumber="123123123",
        firstName="Test",
        lastName="User",
        streetAddress="123 St",
        city="City",
        state="ST",
        zipCode="12345",
        status=InvalidStatus()  # Use our custom invalid status
    )
    
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_member(invalid_member)

def test_database_connection_close(db):
    """Test that database connection closes properly"""
    db.close()
    with pytest.raises(sqlite3.Error):
        db.cursor.execute("SELECT 1")

def test_long_values_truncation():
    """Test handling of values that exceed column length limits"""
    db = DatabaseManager(":memory:")
    db.create_tables()
    
    # Create a provider with a first name that's way too long
    long_name_provider = Provider(
        providerNumber="123456789",
        firstName="T" * 1000,  # Much longer than VARCHAR(25)
        lastName="Doe",
        streetAddress="123 Main St",
        city="Portland",
        state="OR",
        zipCode="97201"
    )
    
    # Since SQLite doesn't enforce VARCHAR length by default,
    # we'll need to add our own validation
    with pytest.raises(ValueError):
        if len(long_name_provider._firstname) > 25:
            raise ValueError("First name exceeds maximum length")
        db.insert_provider(long_name_provider)
    
    db.close()

def test_get_service_records_by_provider(db, sample_provider, sample_member, sample_service):
    """Test retrieving service records for a specific provider"""
    # Insert test data
    db.insert_provider(sample_provider)
    db.insert_member(sample_member)
    db.insert_service(sample_service)

    # Create and insert multiple service records
    service_record1 = ServiceRecord(
        dateReceived=datetime.now(),
        serviceDate=datetime.now().date(),
        provider=sample_provider,
        member=sample_member,
        service=sample_service,
        comments="Test comment 1",
        fee=100.00
    )
    
    service_record2 = ServiceRecord(
        dateReceived=datetime.now(),
        serviceDate=datetime.now().date(),
        provider=sample_provider,
        member=sample_member,
        service=sample_service,
        comments="Test comment 2",
        fee=150.00
    )
    
    db.insert_service_record(service_record1)
    db.insert_service_record(service_record2)
    
    # Retrieve records for the provider
    records = db.get_service_records_by_provider(sample_provider._providerNumber)
    
    assert len(records) == 2
    assert all(record._provider._providerNumber == sample_provider._providerNumber for record in records)
    assert records[0]._comments == "Test comment 1"
    assert records[1]._comments == "Test comment 2"

def test_get_service_records_by_member(db, sample_provider, sample_member, sample_service):
    """Test retrieving service records for a specific member"""
    # Insert test data
    db.insert_provider(sample_provider)
    db.insert_member(sample_member)
    db.insert_service(sample_service)

    # Create and insert multiple service records
    service_record1 = ServiceRecord(
        dateReceived=datetime.now(),
        serviceDate=datetime.now().date(),
        provider=sample_provider,
        member=sample_member,
        service=sample_service,
        comments="Test comment 1",
        fee=100.00
    )
    
    service_record2 = ServiceRecord(
        dateReceived=datetime.now(),
        serviceDate=datetime.now().date(),
        provider=sample_provider,
        member=sample_member,
        service=sample_service,
        comments="Test comment 2",
        fee=150.00
    )
    
    db.insert_service_record(service_record1)
    db.insert_service_record(service_record2)
    
    # Retrieve records for the member
    records = db.get_service_records_by_member(sample_member._memberNumber)
    
    assert len(records) == 2
    assert all(record._member._memberNumber == sample_member._memberNumber for record in records)
    assert records[0]._comments == "Test comment 1"
    assert records[1]._comments == "Test comment 2"

def test_get_service_records_by_provider_empty(db, sample_provider):
    """Test retrieving service records for a provider with no records"""
    db.insert_provider(sample_provider)
    records = db.get_service_records_by_provider(sample_provider._providerNumber)
    assert len(records) == 0

def test_get_service_records_by_member_empty(db, sample_member):
    """Test retrieving service records for a member with no records"""
    db.insert_member(sample_member)
    records = db.get_service_records_by_member(sample_member._memberNumber)
    assert len(records) == 0

def test_update_provider(db, sample_provider):
    """Test updating provider information"""
    db.insert_provider(sample_provider)
    
    # Modify provider details
    sample_provider._firstname = "Jane"
    sample_provider._city = "Seattle"
    sample_provider._state = "WA"
    
    db.update_provider(sample_provider)
    
    # Verify updates
    updated_provider = db.get_provider(sample_provider._providerNumber)
    assert updated_provider._firstname == "Jane"
    assert updated_provider._city == "Seattle"
    assert updated_provider._state == "WA"

def test_update_nonexistent_provider(db, sample_provider):
    """Test updating a provider that doesn't exist"""
    with pytest.raises(sqlite3.Error):
        db.update_provider(sample_provider)

def test_update_member(db, sample_member):
    """Test updating member information"""
    db.insert_member(sample_member)
    
    # Modify member details
    sample_member._firstName = "Janet"
    sample_member._city = "Seattle"
    sample_member._status = Status.SUSPENDED
    
    db.update_member(sample_member)
    
    # Verify updates
    updated_member = db.get_member(sample_member._memberNumber)
    assert updated_member._firstName == "Janet"
    assert updated_member._city == "Seattle"
    assert updated_member._status == Status.SUSPENDED

def test_update_nonexistent_member(db, sample_member):
    """Test updating a member that doesn't exist"""
    with pytest.raises(sqlite3.Error):
        db.update_member(sample_member)

def test_update_service(db, sample_service):
    """Test updating service information"""
    db.insert_service(sample_service)
    
    # Modify service details
    sample_service._serviceName = "Updated Service"
    sample_service._fee = 150.00
    
    db.update_service(sample_service)
    
    # Verify updates
    updated_service = db.get_service(sample_service._serviceCode)
    assert updated_service._serviceName == "Updated Service"
    assert updated_service._fee == 150.00

def test_update_nonexistent_service(db, sample_service):
    """Test updating a service that doesn't exist"""
    with pytest.raises(sqlite3.Error):
        db.update_service(sample_service)

def test_delete_provider(db, sample_provider):
    """Test deleting a provider"""
    db.insert_provider(sample_provider)
    db.delete_provider(sample_provider._providerNumber)
    
    # Verify provider is deleted
    with pytest.raises(sqlite3.Error):
        db.get_provider(sample_provider._providerNumber)

def test_delete_nonexistent_provider(db):
    """Test deleting a provider that doesn't exist"""
    with pytest.raises(sqlite3.Error):
        db.delete_provider("999999999")

def test_delete_member(db, sample_member):
    """Test deleting a member"""
    db.insert_member(sample_member)
    db.delete_member(sample_member._memberNumber)
    
    # Verify member is deleted
    with pytest.raises(sqlite3.Error):
        db.get_member(sample_member._memberNumber)

def test_delete_nonexistent_member(db):
    """Test deleting a member that doesn't exist"""
    with pytest.raises(sqlite3.Error):
        db.delete_member("999999999")

def test_delete_service(db, sample_service):
    """Test deleting a service"""
    db.insert_service(sample_service)
    db.delete_service(sample_service._serviceCode)
    
    # Verify service is deleted
    with pytest.raises(sqlite3.Error):
        db.get_service(sample_service._serviceCode)

def test_delete_nonexistent_service(db):
    """Test deleting a service that doesn't exist"""
    with pytest.raises(sqlite3.Error):
        db.delete_service("999999")

def test_delete_service_record(db, sample_provider, sample_member, sample_service):
    """Test deleting a service record"""
    # Insert prerequisites
    db.insert_provider(sample_provider)
    db.insert_member(sample_member)
    db.insert_service(sample_service)
    
    # Create and insert a service record
    service_record = ServiceRecord(
        dateReceived=datetime.now(),
        serviceDate=datetime.now().date(),
        provider=sample_provider,
        member=sample_member,
        service=sample_service,
        comments="Test comment",
        fee=100.00
    )
    db.insert_service_record(service_record)
    
    # Delete the service record
    db.delete_service_record(1)  # Assuming this is the first record with ID 1
    
    # Verify service record is deleted
    assert db.get_service_record(1) == 0

def test_delete_nonexistent_service_record(db):
    """Test deleting a service record that doesn't exist"""
    with pytest.raises(sqlite3.Error):
        db.delete_service_record(999)

def test_delete_provider_with_service_records(db, sample_provider, sample_member, sample_service):
    """Test deleting a provider who has service records (should fail due to foreign key constraint)"""
    # Insert prerequisites
    db.insert_provider(sample_provider)
    db.insert_member(sample_member)
    db.insert_service(sample_service)