import os               # File IO
import re               # Regex (idx might come in handy, it's good to have too many then too little)
import logging          # Nice interface for logging, just captures timestamp and formats nice
from classes import *
import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self, filename: str):
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()
        # Enable foreign keys and strict string length checking
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.cursor.execute("PRAGMA strict = ON")

    def create_tables(self):
        self.create_provider_table()
        self.create_member_table()
        self.create_services_table()
        self.create_service_records_table()


    def create_provider_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS providers (
                provider_number VARCHAR(9) PRIMARY KEY,
                first_name VARCHAR(25) NOT NULL,
                last_name VARCHAR(25) NOT NULL,
                street_address VARCHAR(25),
                city VARCHAR(14),
                state VARCHAR(2),
                zipcode VARCHAR(5)
            )
        """)


    def create_member_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_number VARCHAR(9) PRIMARY KEY,
                first_name VARCHAR(25) NOT NULL,
                last_name VARCHAR(25) NOT NULL,
                street_address VARCHAR(25),
                city VARCHAR(14),
                state VARCHAR(2),
                zipcode VARCHAR(5),
                status TEXT CHECK(status IN ('VALID', 'SUSPENDED', 'INVALID')) NOT NULL DEFAULT 'VALID'
            )
        """)


    def create_services_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                service_code VARCHAR(6) PRIMARY KEY,
                service_name VARCHAR(20) NOT NULL,
                fee DECIMAL(8,2) NOT NULL
            )
        """)


    def create_service_records_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS service_records (
                service_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_received DATETIME NOT NULL,
                service_date DATE NOT NULL,
                provider_number VARCHAR(9) NOT NULL,
                member_number VARCHAR(9) NOT NULL,
                service_code VARCHAR(6) NOT NULL,
                comments VARCHAR(100),
                fee DECIMAL(8,2) NOT NULL,
                FOREIGN KEY (provider_number) REFERENCES providers(provider_number),
                FOREIGN KEY (member_number) REFERENCES members(member_number),
                FOREIGN KEY (service_code) REFERENCES services(service_code)
            )
        """)
    

    def insert_provider(self, provider: Provider):
        # Validate field lengths
        if len(provider._firstname) > 25:
            raise ValueError("First name exceeds maximum length of 25 characters")
        if len(provider._lastname) > 25:
            raise ValueError("Last name exceeds maximum length of 25 characters")
        if len(provider._streetAddress) > 25:
            raise ValueError("Street address exceeds maximum length of 25 characters")
        if len(provider._city) > 14:
            raise ValueError("City exceeds maximum length of 14 characters")
        if len(provider._state) > 2:
            raise ValueError("State exceeds maximum length of 2 characters")
        if len(provider._zipCode) > 5:
            raise ValueError("Zip code exceeds maximum length of 5 characters")

        self.cursor.execute("""
            INSERT INTO providers (
                provider_number,
                first_name,
                last_name,
                street_address,
                city,
                state,
                zipcode
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            provider._providerNumber,
            provider._firstname,
            provider._lastname,
            provider._streetAddress,
            provider._city,
            provider._state,
            provider._zipCode
        ))
        self.conn.commit()


    def insert_member(self, member: Member):
        self.cursor.execute("""
            INSERT INTO members (
                member_number,
                first_name,
                last_name,
                street_address,
                city,
                state,
                zipcode,
                status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            member._memberNumber,
            member._firstName,
            member._lastName,
            member._streetAddress,
            member._city,
            member._state,
            member._zipCode,
            member._status.name
        ))
        self.conn.commit()


    def insert_service(self, service: Service):
        self.cursor.execute("""
            INSERT INTO services (
                service_code,
                service_name,
                fee
            ) VALUES (?, ?, ?)
        """, (
            service._serviceCode,
            service._serviceName, 
            service._fee
        ))
        self.conn.commit()

    
    def insert_service_record(self, service_record: ServiceRecord):
        try:
            self.cursor.execute("""
                INSERT INTO service_records (
                    date_received,
                    service_date,
                    provider_number,
                    member_number,
                    service_code,
                    comments,
                    fee
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                service_record._dateReceived.isoformat(),  # Convert datetime to string
                service_record._serviceDate.isoformat(),   # Convert date to string
                service_record._provider._providerNumber,
                service_record._member._memberNumber,
                service_record._service._serviceCode,
                service_record._comments,
                service_record._fee
            ))
            self.conn.commit()
        except sqlite3.Error as e:
            if "FOREIGN KEY constraint failed" in str(e):
                raise sqlite3.IntegrityError("Foreign key constraint failed")
            raise e


    def get_provider(self, provider_number: str) -> Provider:
        self.cursor.execute("SELECT * FROM providers WHERE provider_number = ?", (provider_number,))
        row = self.cursor.fetchone()
        if row is None:
            raise sqlite3.Error(f"No provider found with number {provider_number}")
        return Provider(
            providerNumber=row[0],
            firstName=row[1],
            lastName=row[2],
            streetAddress=row[3],
            city=row[4],
            state=row[5],
            zipCode=row[6]
        )
    

    def get_member(self, member_number: str) -> Member:
        self.cursor.execute("SELECT * FROM members WHERE member_number = ?", (member_number,))
        row = self.cursor.fetchone()
        if row is None:
            raise sqlite3.Error(f"No member found with number {member_number}")
        return Member(
            memberNumber=row[0],
            firstName=row[1],
            lastName=row[2],
            streetAddress=row[3],
            city=row[4],
            state=row[5],
            zipCode=row[6],
            status=Status[row[7]]  # This will convert 'VALID' to Status.VALID
        )
    

    def get_service(self, service_code: str) -> Service:
        self.cursor.execute("SELECT * FROM services WHERE service_code = ?", (service_code,))
        row = self.cursor.fetchone()
        if row is None:
            raise sqlite3.Error(f"No service found with code {service_code}")
        return Service(
            serviceCode=row[0],
            serviceName=row[1],
            fee=row[2]
        )
    

    def get_service_record(self, service_record_id: int) -> ServiceRecord:
        self.cursor.execute("""
            SELECT 
                sr.service_record_id,
                sr.date_received,
                sr.service_date,
                sr.provider_number,
                sr.member_number,
                sr.service_code,
                sr.comments,
                sr.fee,
                p.first_name as provider_first_name,
                p.last_name as provider_last_name,
                p.street_address as provider_street,
                p.city as provider_city,
                p.state as provider_state,
                p.zipcode as provider_zip,
                m.first_name as member_first_name,
                m.last_name as member_last_name,
                m.street_address as member_street,
                m.city as member_city,
                m.state as member_state,
                m.zipcode as member_zip,
                m.status as member_status,
                s.service_name,
                s.fee as service_fee
            FROM service_records sr
            JOIN providers p ON sr.provider_number = p.provider_number
            JOIN members m ON sr.member_number = m.member_number
            JOIN services s ON sr.service_code = s.service_code
            WHERE sr.service_record_id = ?
        """, (service_record_id,))
        row = self.cursor.fetchone()
        if row is None:
            raise sqlite3.Error(f"No service record found with ID {service_record_id}")
        
        # Create Provider, Member and Service objects from the joined data
        provider = Provider(
            providerNumber=row[3],
            firstName=row[8],
            lastName=row[9],
            streetAddress=row[10],
            city=row[11],
            state=row[12],
            zipCode=row[13]
        )
        
        member = Member(
            memberNumber=row[4],
            firstName=row[14],
            lastName=row[15],
            streetAddress=row[16],
            city=row[17],
            state=row[18],
            zipCode=row[19],
            status=Status[row[20]]
        )
        
        service = Service(
            serviceCode=row[5],
            serviceName=row[21],
            fee=row[22]
        )
        
        # Create and return ServiceRecord
        return ServiceRecord(
            dateReceived=datetime.fromisoformat(row[1]),
            serviceDate=datetime.fromisoformat(row[2]).date(),
            provider=provider,
            member=member,
            service=service,
            comments=row[6],
            fee=row[7]
        )
    
    def close(self):
        self.conn.close()