import os               # File IO
import re               # Regex (idx might come in handy, it's good to have too many then too little)
import logging          # Nice interface for logging, just captures timestamp and formats nice
from dataclasses import dataclass, field # Class helpers, py 3.8+ features that make classes much shorter to write
from typing import *    # Type hinting
from classes import *
import sqlite3


class DatabaseManager:
    def __init__(self, filename: str):
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

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
                status TEXT CHECK(status IN ('Valid', 'Suspended', 'Invalid')) NOT NULL DEFAULT 'Valid'
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
                datareceived_datetime DATETIME NOT NULL,
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
            provider._name.split()[0],  # First name
            provider._name.split()[-1], # Last name 
            provider._streetAddress,
            provider._city,
            provider._state,
            provider._zipCode
        ))
        self.connection.commit()


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
            member._status.value
        ))
        self.connection.commit()


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
        self.connection.commit()

    
    def insert_service_record(self, service_record: ServiceRecord):
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
            service_record._dateReceived,
            service_record._serviceDate,
            service_record._provider._providerNumber,
            service_record._member._memberNumber,
            service_record._service._serviceCode,
            service_record._comments,
            service_record._fee
        ))
        self.connection.commit()


    def get_provider(self, provider_number: str) -> Provider:
        self.cursor.execute("SELECT * FROM providers WHERE provider_number = ?", (provider_number,))
        return Provider(*self.cursor.fetchone())
    

    def get_member(self, member_number: str) -> Member:
        self.cursor.execute("SELECT * FROM members WHERE member_number = ?", (member_number,))
        return Member(*self.cursor.fetchone())
    

    def get_service(self, service_code: str) -> Service:
        self.cursor.execute("SELECT * FROM services WHERE service_code = ?", (service_code,))
        return Service(*self.cursor.fetchone())
    

    def get_service_record(self, service_record_id: int) -> ServiceRecord:
        self.cursor.execute("SELECT * FROM service_records WHERE service_record_id = ?", (service_record_id,))
        return ServiceRecord(*self.cursor.fetchone())
    
    
    def close(self):
        self.conn.close()