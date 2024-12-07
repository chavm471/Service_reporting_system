from enum import Enum
from datetime import date
import os               # File IO
import re               # Regex (idx might come in handy, it's good to have too many then too little)
import logging          # Nice interface for logging, just captures timestamp and formats nice
from dataclasses import dataclass, field # Class helpers, py 3.8+ features that make classes much shorter to write
from typing import *    # Type hinting
from datetime import datetime

class Status(Enum):
    VALID = 1
    SUSPENDED = 2
    INVALID = 3

class Member:
    def __init__(self, memberNumber: str = None, firstName: str = None, lastName: str = None, 
                 streetAddress: str = None, city: str = None, state: str = None, 
                 zipCode: str = None, status: Status = Status.INVALID) -> None:
        self._memberNumber = memberNumber
        self._firstName = firstName
        self._lastName = lastName
        self._streetAddress = streetAddress
        self._city = city
        self._state = state
        self._zipCode = zipCode
        self._status = status

    @classmethod
    def prompt_member_constructor(self):
        # Create a new member by prompting for each field
        member_number = input("Enter member number (9 digits): ")
        while not re.match(r"^\d{9}$", member_number):
            print("Invalid member number. Must be exactly 9 digits")
            member_number = input("Enter member number (9 digits): ")

        first_name = input("Enter first name: ")
        while not first_name:
            print("First name cannot be empty")
            first_name = input("Enter first name: ")

        last_name = input("Enter last name: ")
        while not last_name:
            print("Last name cannot be empty") 
            last_name = input("Enter last name: ")

        street_address = input("Enter street address: ")
        while not street_address:
            print("Street address cannot be empty")
            street_address = input("Enter street address: ")

        city = input("Enter city: ")
        while not city:
            print("City cannot be empty")
            city = input("Enter city: ")

        state = input("Enter state (2 letters): ")
        while not re.match(r"^[A-Z]{2}$", state.upper()):
            print("Invalid state. Must be exactly 2 letters")
            state = input("Enter state (2 letters): ")

        zip_code = input("Enter ZIP code (5 digits): ")
        while not re.match(r"^\d{5}$", zip_code):
            print("Invalid ZIP code. Must be exactly 5 digits")
            zip_code = input("Enter ZIP code (5 digits): ")

        # Create and return new Member object with validated inputs
        return Member(
            memberNumber=member_number,
            firstName=first_name,
            lastName=last_name,
            streetAddress=street_address,
            city=city,
            state=state.upper(),
            zipCode=zip_code,
            status=Status.VALID
        )

    def validate(self):
        pass
    
    #updates the members status
    def updateStatus(self,newStatus):
        pass
    
    def __repr__(self) -> str:
        return f"Member Number: {self._memberNumber}\nFirst Name: {self._firstName}\nLast Name: {self._lastName}\nAddress: {self._streetAddress} {self._city} {self._state} {self._zipCode}\nMembership Status: {self._status}"

    def update(self):
        """Update member information through user prompts"""
        selection = 0
        print("Select Member Field to Update\n")
        print("1. First Name")
        print("2. Last Name")
        print("3. Street Address")
        print("4. City")
        print("5. State")
        print("6. Zip Code")
        print("7. Status")
        
        while selection < 1 or selection > 7:
            selection = int(input("Selection: "))
            
        if selection == 1:
            self._firstName = input("Updated First Name: ").strip()
            while not self._firstName:
                self._firstName = input("Please Enter Valid First Name: ").strip()
        elif selection == 2:
            self._lastName = input("Updated Last Name: ").strip()
            while not self._lastName:
                self._lastName = input("Please Enter Valid Last Name: ").strip()
        elif selection == 3:
            self._streetAddress = input("Update Street Address: ").strip()
            while not self._streetAddress:
                self._streetAddress = input("Please Enter Valid Street Address: ").strip()
        elif selection == 4:
            self._city = input("Updated City: ").strip()
            while not self._city:
                self._city = input("Please Enter Valid City: ").strip()
        elif selection == 5:
            self._state = input("Updated Two Letter State ID: ").strip().upper()
            while not re.match(r"^[A-Z]{2}$", self._state):
                self._state = input("Please Enter Valid Two Letter State ID: ").strip().upper()
        elif selection == 6:
            self._zipCode = input("Updated Five Digit Zipcode: ").strip()
            while not re.match(r"^\d{5}$", self._zipCode):
                self._zipCode = input("Please Enter Valid Five Digit Zip Code: ").strip()
        elif selection == 7:
            status_input = input("Updated Status (VALID/SUSPENDED/INVALID): ").upper()
            while status_input not in ["VALID", "SUSPENDED", "INVALID"]:
                status_input = input("Please Enter Valid Status (VALID/SUSPENDED/INVALID): ").upper()
            self._status = Status[status_input]

    def generate_report(self, db_manager):
        """Generate a report for this member"""
        filename = f"member_{self._memberNumber}_report.txt"
        original = sys.stdout
        with open(filename, "w") as f:
            sys.stdout = f
            print(repr(self))
            print("\nServices:")
            services = db_manager.get_service_records_by_member(self._memberNumber)
            for service in services:
                service.displayInfo()
        sys.stdout = original

class Provider:
    def __init__(self, providerNumber: str = None, firstName: str = None, lastName: str = None, streetAddress: str = None, city: str = None, state: str = None, zipCode: str = None) -> None:
        self._providerNumber = providerNumber
        self._firstname = firstName
        self._lastname = lastName
        self._streetAddress = streetAddress
        self._city = city
        self._state = state
        self._zipCode = zipCode

    @classmethod
    def prompt_provider_constructor(self):
        # Get and validate provider number
        provider_number = input("Enter provider number (9 digits): ")
        while not re.match(r"^\d{9}$", provider_number):
            print("Invalid provider number. Must be exactly 9 digits")
            provider_number = input("Enter provider number (9 digits): ")

        # Get and validate first name
        first_name = input("Enter first name: ")
        while not first_name:
            print("First name cannot be empty")
            first_name = input("Enter first name: ")

        # Get and validate last name  
        last_name = input("Enter last name: ")
        while not last_name:
            print("Last name cannot be empty")
            last_name = input("Enter last name: ")

        # Get and validate street address
        street_address = input("Enter street address: ")
        while not street_address:
            print("Street address cannot be empty")
            street_address = input("Enter street address: ")

        # Get and validate city
        city = input("Enter city: ")
        while not city:
            print("City cannot be empty") 
            city = input("Enter city: ")

        # Get and validate state
        state = input("Enter state (2 letters): ")
        while not re.match(r"^[A-Z]{2}$", state.upper()):
            print("Invalid state. Must be exactly 2 letters")
            state = input("Enter state (2 letters): ")

        # Get and validate ZIP code
        zip_code = input("Enter ZIP code (5 digits): ")
        while not re.match(r"^\d{5}$", zip_code):
            print("Invalid ZIP code. Must be exactly 5 digits")
            zip_code = input("Enter ZIP code (5 digits): ")

        # Create and return new Provider object with validated inputs
        return Provider(
            providerNumber=provider_number,
            firstName=first_name,
            lastName=last_name,
            streetAddress=street_address,
            city=city,
            state=state.upper(),
            zipCode=zip_code
        )

    def validate(self):
        pass

    def recordService(serviceRecord):
        #append service Recorded to serviceRecord
        #print "service recorded successfully"
        pass

    def requestProviderDirectory(self):
        #serviceList = Query all entries in services table
        #return servicesList
        pass
    
    def generateReport(self):
        #reportData = Retrieve ServiceRecords where
        #ProviderNumber == self._providernumber
        pass

    def __repr__(self) -> str:
        return f"Provider Number: {self._providerNumber}\nName: {self._firstname} {self._lastname}\nAddress: {self._streetAddress} {self._city} {self._state} {self._zipCode}"

    def update(self):
        """Update provider information through user prompts"""
        selection = 0
        print("Select Provider Field to Update\n")
        print("1. First Name")
        print("2. Last Name")
        print("3. Street Address")
        print("4. City")
        print("5. State")
        print("6. Zip Code")
        
        while selection < 1 or selection > 6:
            selection = int(input("Selection: "))
            
        if selection == 1:
            self._firstname = input("Updated First Name: ").strip()
            while not self._firstname:
                self._firstname = input("Please Enter Valid First Name: ").strip()
        elif selection == 2:
            self._lastname = input("Updated Last Name: ").strip()
            while not self._lastname:
                self._lastname = input("Please Enter Valid Last Name: ").strip()
        elif selection == 3:
            self._streetAddress = input("Update Street Address: ").strip()
            while not self._streetAddress:
                self._streetAddress = input("Please Enter Valid Street Address: ").strip()
        elif selection == 4:
            self._city = input("Updated City: ").strip()
            while not self._city:
                self._city = input("Please Enter Valid City: ").strip()
        elif selection == 5:
            self._state = input("Updated Two Letter State ID: ").strip().upper()
            while not re.match(r"^[A-Z]{2}$", self._state):
                self._state = input("Please Enter Valid Two Letter State ID: ").strip().upper()
        elif selection == 6:
            self._zipCode = input("Updated Five Digit Zipcode: ").strip()
            while not re.match(r"^\d{5}$", self._zipCode):
                self._zipCode = input("Please Enter Valid Five Digit Zip Code: ").strip()

    def generate_report(self, db_manager):
        """Generate a report for this provider"""
        filename = f"provider_{self._providerNumber}_report.txt"
        original_std = sys.stdout
        with open(filename, "w") as f:
            sys.stdout = f
            print(repr(self))
            print("\nServices:")
            try:
                service_list = db_manager.get_service_records_by_provider(self._providerNumber)
                consultations = 0
                total_fee = 0
                for service in service_list:
                    service.displayInfo()
                    consultations += 1
                    total_fee += service._fee
                print(f"\nTotal consultations: {consultations}")
                print(f"Total fees: ${total_fee:.2f}")
            except Exception as e:
                print(f"Error generating provider report: {e}")
        sys.stdout = original_std

class Service:
    def __init__(self, serviceCode: str = None, serviceName: str = None, fee: float = None) -> None:
        self._serviceCode = serviceCode
        self._serviceName = serviceName 
        self._fee = fee

    #show service details
    def __repr__(self) -> str:
        return f"Service Name: {self._serviceName}\nService Code: {self._serviceCode}\nFee: {self._fee}"

class ServiceRecord:
    def __init__(self, dateReceived=None, serviceDate=None, provider=None, member=None, service=None, comments=None, fee=None) -> None:
        self._recordID:int = None
        self._dateReceived = dateReceived if dateReceived else date.today()
        self._serviceDate = serviceDate if serviceDate else date.today()
        self._provider = provider
        self._member = member 
        self._service = service
        self._comments = comments
        self._fee = fee

    # Do we actually need this function ?? - Gil
    #initializes a new service record. 
    def createRecord(self):
        #recordId = GenerateUniqueID()
        #dateReceived = date.today()
        #save record to database
        pass
    
    #displays the service record details
    def displayInfo(self):
        print("Record ID:",self._recordID)
        print("Date Received:",self._dateReceived)
        print("Provider:",self._provider)
        print("Member:",self._member)
        print("Comments:",self._comments)
        print("Fee:",self._fee)

    def update(self):
        """Update service record information through user prompts"""
        print("\nSelect field to update:")
        print("1. Service Date")
        print("2. Comments")
        print("3. Fee")
        
        selection = input("Selection: ")
        while not selection.isdigit() or int(selection) < 1 or int(selection) > 3:
            selection = input("Please enter a valid selection (1-3): ")
        
        selection = int(selection)
        
        if selection == 1:
            date_input = input("New Service Date (YYYY-MM-DD): ")
            self._serviceDate = datetime.strptime(date_input, "%Y-%m-%d")
        elif selection == 2:
            comments = input("New Comments (max 100 characters): ")
            while len(comments) > 100:
                print("Comments too long. Maximum 100 characters.")
                comments = input("New Comments (max 100 characters): ")
            self._comments = comments
        elif selection == 3:
            fee = input("New Fee (max 8 digits, 2 decimal places): ")
            while not re.match(r"^\d{1,8}(\.\d{0,2})?$", fee):
                print("Invalid fee format.")
                fee = input("New Fee (max 8 digits, 2 decimal places): ")
            self._fee = float(fee)

class ChocAnSystem:
    def __init__(self) -> None:
        from database import DatabaseManager
        self._DB = DatabaseManager("chocoDB")
        self._members = self._DB.get_member_directory()
        self._providers = self._DB.get_provider_directory()
        self._services = self._DB.get_service_directory()

    def updateMember(self):
        mem_num = input("Enter Member Number to Update: ")
        try:
            member = self._DB.get_member(mem_num)
            member.update()
            self._DB.update_member(member)
        except Exception as e:
            print(f"Error updating member: {e}")

    def updateProvider(self):
        prov_num = input("Enter Provider Number to Update: ")
        try:
            provider = self._DB.get_provider(prov_num)
            provider.update()
            self._DB.update_provider(provider)
        except Exception as e:
            print(f"Error updating provider: {e}")

    def updateServiceRecord(self):
        record_id = input("Enter Service Record ID to Update: ")
        try:
            record = self._DB.get_service_record(record_id)
            record.update()
            self._DB.update_service_record(record)
        except Exception as e:
            print(f"Error updating service record: {e}")

    def generateWeeklyReports(self):
        try:
            print("*** Generating Weekly Reports ***")
            print("\nProvider Reports:")
            for provider in self._providers:
                provider.generate_report(self._DB)
            
            print("\nMember Reports:")
            for member in self._members:
                member.generate_report(self._DB)
            
            print("\nWeekly reports generation complete.")
        except Exception as e:
            print(f"Error generating weekly reports: {e}")
