from classes import *
import sqlite3
from datetime import datetime

class DatabaseManager:
    """
    Manages SQLite database operations for the ChocAn system.

    This class handles all database interactions including creating tables, inserting,
    retrieving, and updating records for providers, members, services, and service records.
    It implements data validation and maintains referential integrity through foreign key
    constraints.

    Attributes:
        conn: SQLite database connection object
        cursor: Database cursor for executing SQL commands

    Tables:
        - providers: Stores healthcare provider information
        - members: Stores ChocAn member information with status
        - services: Stores available healthcare services and fees
        - service_records: Stores records of services provided to members

    Methods:
        __init__(filename: str) -> None        
        create_tables() -> None        
        check_provider(provider: Provider) -> None
            Validates provider data fields length. Raises ValueError if invalid
            This is a helper function for insert_provider()

        # CREATE METHODS (YOU CAN IGNORE THESE)
        create_provider_table() -> None        
        create_member_table() -> None
        create_services_table() -> None        
        create_service_records_table() -> None        

        # INSERT METHODS TODO: RETURN THE ID's
        insert_provider(provider: Provider) -> None
        insert_member(member: Member) -> None
        insert_service(service: Service) -> None
        insert_service_record(service_record: ServiceRecord) -> None

        # GET METHODS
        get_provider(provider_number: str) -> Provider
            Retrieves provider by number. Raises sqlite3.Error if not found
        get_member(member_number: str) -> Member
            Retrieves member by number. Raises sqlite3.Error if not found
        get_service(service_code: str) -> Service
            Retrieves service by code. Raises sqlite3.Error if not found
        get_service_record(service_record_id: int) -> ServiceRecord
            Retrieves service record by ID. Raises sqlite3.Error if not found
        get_service_records_by_provider(provider_number: str) -> list[ServiceRecord]
            Retrieves all service records for a given provider number. [] if none found
        get_service_records_by_member(member_number: str) -> list[ServiceRecord]
            Retrieves all service records for a given member number. [] if none found
        
        # UPDATE METHODS
        update_provider(provider: Provider) -> None
            Updates existing provider. Raises sqlite3.Error if not found
        update_member(member: Member) -> None
            Updates existing member. Raises sqlite3.Error if not found
        update_service(service: Service) -> None
            Updates existing service. Raises sqlite3.Error if not found
        
        # DELETE METHODS
        delete_provider(provider_number: str) -> None
            Deletes existing provider. Raises sqlite3.Error if not found
        delete_member(member_number: str) -> None
            Deletes existing member. Raises sqlite3.Error if not found
        delete_service(service_code: str) -> None
            Deletes existing service. Raises sqlite3.Error if not found
        delete_service_record(service_record_id: int) -> None
            Deletes existing service record. Raises sqlite3.Error if not found
        
        close() -> None
            Closes the database connection

    Usage:
        db = DatabaseManager('chocan.db')
        db.create_tables()
        # Perform database operations
        db.close()
    """

    def __init__(self, filename: str):
        try:
            self.conn = sqlite3.connect(filename)
            self.cursor = self.conn.cursor()
            # Enable foreign keys and strict string length checking
            self.cursor.execute("PRAGMA foreign_keys = ON")
            self.cursor.execute("PRAGMA strict = ON")
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to initialize database connection: {str(e)}")

    def create_tables(self):
        self.create_provider_table()
        self.create_member_table()
        self.create_services_table()
        self.create_service_records_table()
        

    def check_provider(self, provider: Provider):
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
                date_received DATE NOT NULL,
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
    
    #add a provider
    def insert_provider(self, provider: Provider):
        self.check_provider(provider)
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
            #members of the provider, inserting each into database
            provider._providerNumber,
            provider._firstname,
            provider._lastname,
            provider._streetAddress,
            provider._city,
            provider._state,
            provider._zipCode
        ))
        #committing to the database (inserting)
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
    
    def get_member_directory(self) -> list[Member]:
        self.cursor.execute("SELECT * FROM members")
        rows = self.cursor.fetchall()
        return [Member(
            memberNumber=row[0],
            firstName=row[1],
            lastName=row[2],
            streetAddress=row[3],
            city=row[4],
            state=row[5],
            zipCode=row[6],
            status=Status[row[7]]
        ) for row in rows]

    def get_provider_directory(self) -> list[Provider]:
        self.cursor.execute("""SELECT provider_number, first_name, last_name, street_address, city, state, zipcode
        FROM providers""")
        rows = self.cursor.fetchall()
        return [Provider(*row) for row in rows]
    
    def get_service_records_by_provider(self, provider_number: str) -> list[ServiceRecord]:
        """
        Retrieves all service records for a given provider number.
        
        Args:
            provider_number: The provider's unique identifier
            
        Returns:
            List of ServiceRecord objects
            
        Raises:
            sqlite3.Error: If provider not found or database error occurs
        """
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
            WHERE sr.provider_number = ?
            ORDER BY sr.service_date DESC
        """, (provider_number,))
        
        rows = self.cursor.fetchall()
        if not rows:
            return []
        
        service_records = []
        for row in rows:
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
            
            service_record = ServiceRecord(
                dateReceived=datetime.fromisoformat(row[1]),
                serviceDate=datetime.fromisoformat(row[2]).date(),
                provider=provider,
                member=member,
                service=service,
                comments=row[6],
                fee=row[7]
            )
            service_records.append(service_record)
        
        return service_records
    
    def get_service_records_by_member(self, member_number: str) -> list[ServiceRecord]:
        """
        Retrieves all service records for a given member number.
        
        Args:
            member_number: The member's unique identifier
            
        Returns:
            List of ServiceRecord objects, [] if no records found
        """
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
            WHERE sr.member_number = ?
            ORDER BY sr.service_date DESC
        """, (member_number,))
        
        rows = self.cursor.fetchall()
        if not rows:
            return []
        
        service_records = []
        for row in rows:
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
            
            service_record = ServiceRecord(
                dateReceived=datetime.fromisoformat(row[1]),
                serviceDate=datetime.fromisoformat(row[2]).date(),
                provider=provider,
                member=member,
                service=service,
                comments=row[6],
                fee=row[7]
            )
            service_records.append(service_record)
        
        return service_records

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
            return 0
        
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
    
    def update_provider(self, provider: Provider):
        self.check_provider(provider)
        self.cursor.execute("""
            UPDATE providers 
            SET first_name = ?,
                last_name = ?,
                street_address = ?,
                city = ?,
                state = ?,
                zipcode = ?
            WHERE provider_number = ?
        """, (
            provider._firstname,
            provider._lastname,
            provider._streetAddress,
            provider._city,
            provider._state,
            provider._zipCode,
            provider._providerNumber
        ))
        if self.cursor.rowcount == 0:
            raise sqlite3.Error(f"No provider found with number {provider._providerNumber}")
        self.conn.commit()

    def update_member(self, member: Member):
        self.cursor.execute("""
            UPDATE members 
            SET first_name = ?,
                last_name = ?,
                street_address = ?,
                city = ?,
                state = ?,
                zipcode = ?,
                status = ?
            WHERE member_number = ?
        """, (
            member._firstName,
            member._lastName,
            member._streetAddress,
            member._city,
            member._state,
            member._zipCode,
            member._status.name,
            member._memberNumber
        ))
        if self.cursor.rowcount == 0:
            raise sqlite3.Error(f"No member found with number {member._memberNumber}")
        self.conn.commit()
    
    def update_service(self, service: Service):
        self.cursor.execute("""
            UPDATE services 
            SET service_name = ?,
                fee = ?
            WHERE service_code = ?
        """, (
            service._serviceName,
            service._fee,
            service._serviceCode
        ))
        if self.cursor.rowcount == 0:
            raise sqlite3.Error(f"No service found with code {service._serviceCode}")
        self.conn.commit()

    def delete_provider(self, provider_number: str) -> None:
        self.cursor.execute("DELETE FROM providers WHERE provider_number = ?", (provider_number,))
        if self.cursor.rowcount == 0:
            raise sqlite3.Error(f"No provider found with number {provider_number}")
        self.conn.commit()

    def delete_member(self, member_number: str) -> None:
        self.cursor.execute("DELETE FROM members WHERE member_number = ?", (member_number,))
        if self.cursor.rowcount == 0:
            raise sqlite3.Error(f"No member found with number {member_number}")
        self.conn.commit()

    def delete_service(self, service_code: str) -> None:
        self.cursor.execute("DELETE FROM services WHERE service_code = ?", (service_code,))
        if self.cursor.rowcount == 0:
            raise sqlite3.Error(f"No service found with code {service_code}")
        self.conn.commit()

    def delete_service_record(self, service_record_id: int) -> None:
        self.cursor.execute("DELETE FROM service_records WHERE service_record_id = ?", (service_record_id,))
        if self.cursor.rowcount == 0:
            raise sqlite3.Error(f"No service record found with ID {service_record_id}")
        self.conn.commit()
    

    def close(self):
        self.conn.close()

    # Auto close the connection when this instance dies. 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_service_directory(self) -> list[Service]:
        self.cursor.execute("SELECT * FROM services")
        rows = self.cursor.fetchall()
        return [Service(
            serviceCode=row[0],
            serviceName=row[1],
            fee=row[2]
        ) for row in rows]