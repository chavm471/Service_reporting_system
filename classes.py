from enum import Enum
from datetime import date
import os               # File IO
import re               # Regex (idx might come in handy, it's good to have too many then too little)
import logging          # Nice interface for logging, just captures timestamp and formats nice
from dataclasses import dataclass, field # Class helpers, py 3.8+ features that make classes much shorter to write
from typing import *    # Type hinting
from datetime import datetime
import sqlite3
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
    
    # updates the members status
    def updateStatus(self,newStatus):
        pass
    
    def __repr__(self) -> str:
        return f"Member Number: {self._memberNumber}\nFirst Name: {self._firstName}\nLast Name: {self._lastName}\nAddress: {self._streetAddress} {self._city} {self._state} {self._zipCode}\nMembership Status: {self._status}"

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

class ChocAnSystem:
    def __init__(self) -> None:
        from database import DatabaseManager
        self._DB = DatabaseManager("chocoDB")
        self._members = self._DB.get_member_directory()
        self._providers = self._DB.get_provider_directory()
        self._services = self._DB.get_service_directory()


    # print validated if member id is found
    # print Invalid if member id is not found or suspended
    # return valid id or 0 if invalid
    def validateMember(self, member_number: str) -> bool:
        try:
            member = self._DB.get_member(member_number)
            if member._status == Status.VALID:
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(f"Error validating member: {e}")
            return False

    def validateProvider(self):
        pass

    def addMember(self):
        mem = Member()

        # ensure member number is not None, is length 9, and numeric
        mem._memberNumber = input("Nine digit member number: ").strip()
        while not mem._memberNumber.isdigit() or len(mem._memberNumber) != 9:
            mem._memberNumber = input("Please enter a valid nine digit member number: ").strip()

        # ensure first name is not empty
        mem._firstName = input("First name:").strip()
        while not mem._firstName:
            mem._firstName = input("Please enter valid first name:").strip()

        # ensure last name is not empty
        mem._lastName = input("Last name:").strip()
        while not mem._lastName:
            mem._lastName = input("Please enter valid last name:").strip()

        # ensure street address is not empty
        mem._streetAddress = input("Street address: ").strip()
        while not mem._streetAddress:
            mem._streetAddress = input("Please enter valid street address: ").strip()

        # ensure city is not empty
        mem._city = input("City: ").strip()
        while not mem._city:
            mem._city = input("Please enter valid city: ").strip()

        # ensure state is 2 letters
        mem._state = input("Two letter state id: ").strip()
        while len(mem._state) != 2:
            mem._state = input("Please enter valid two letter state id: ").strip()

        # ensure zipcode is 5-digit numeric
        mem._zipCode = input("Five digit zipcode: ").strip()
        while not mem._zipCode.isdigit() or len(mem._zipCode) != 5:
            mem._zipCode = input("Please enter valid five digit zip code: ").strip()

        try:
            self._DB.insert_member(mem)
        except Exception as e:
            print(f"Error adding member: {e}")
    
    # Updates member information
    def updateMember(self):
        mem_num = input("Enter Mumber Number to Update: ")
        member = self._DB.get_member(mem_num)
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
        if(selection == 1):
            member._firstName = input("Updated First Name:")
            while member._firstName is None:
                member._firstName = input("Please Enter Valid First Name:") 
        elif(selection == 2):
            member._lastName = input("Updated Last Name:")
            while member._lastName is None:
                member._lastName = input("Please Enter Valid Last Name:") 
        elif(selection == 3):
            member._streetAddress = input("Update Street Address: ")
            while member._streetAddress is None:
                member._streetAddress = input("Please Enter Valid Street Address: ")
        elif(selection == 4):
            member._city = input("Updated City: ")
            while member._city is None:
                member._city = input("Please Enter Valid City: ")     
        elif(selection == 5):
            member._state = input("Updated Two Letter State ID: ")
            while member._state is None or len(member._city) < 2:
                member._city = input("Please Enter Valid Two Letter State ID: ")
        elif(selection == 6):
            member._zipCode = input("Updated Five Digit Zipcode: ")
            while member._zipCode is None or len(member._zipCode) < 5:
                member._zipCode = input("Please Enter Valid Five Digit Zip Code: ")
        elif(selection == 7):
            member._status = input("Updated Status:")
            while member._status is None:
                member._status = input("Please Enter Valid Status")
        try:
            self._DB.update_member(member)        
        except Exception as e:
            print(f"Error updating member: {e}")

    def deleteMember(self):
        mem_num = input("Please Enter Member Number to Delete: ")
        try:
            self._DB.delete_member(mem_num)
        except Exception as e:
            print(f"Error deleting member: {e}")

    # Adds new provider
    def addProvider(self):
        provider_number = input("Enter provider number (9 digits): ")
        while not re.match(r"^\d{9}$", provider_number):
            print("Invalid provider number. Must be exactly 9 digits")
            provider_number = input("Enter provider number (9 digits): ")
        
        f_name = input("Enter the first name of the provider: ")
        while not re.match(r"^[a-zA-Z]+$",f_name):
            print("Invalid first name. Only letters are allowed.")
        
        l_name = input("Enter the last name of the provider: ")
        while not re.match(r"^[a-zA-Z]+$",l_name):  
            print("Invalid last name. Only letters are allowed.")
            l_name = input("Enter the last name of the provider: ")

        p_str_addr = input("Enter the street address of provider:")
        while not re.match(r"^[a-zA-Z0-9\s,.#-]+$", p_str_addr):
            print("Invalid address. Only letters, numbers, and common address symbols (.,#-) are allowed.")
            p_str_addr = input("Enter the street address of provider: ")

        city = input("Enter the city of provider:")
        while not re.match(r"^[a-zA-Z\s]+$", city):
            print("Invalid city. Only letters and spaces are allowed.")
            city = input("Enter the city of provider: ")

        st = input("Enter the state of the provider (2 letters):")
        while not re.match(r"^[A-Z]{2}$", st):
            print("Invalid state. Enter exactly two uppercase letters (e.g., 'CA').")
            st = input("Enter the state of the provider (e.g., 'CA'): ")


        zip = input("Enter the zipcode of provider:")
        while not re.match(r"^\d{5}$", zip):
            print("Invalid ZIP code. Enter exactly 5 digits.")
            zip = input("Enter the zipcode of provider: ")

        #make a new Provider object
        new_provider = Provider(
            providerNumber=provider_number,
            firstName=f_name,
            lastName=l_name,
            streetAddress=p_str_addr,
            city=city,
            state=st,
            zipCode=zip
        )
        try:
            self._DB.insert_provider(new_provider)
        except Exception as e:
            print(f"Error adding provider: {e}")

    # Updates provider information
    def updateProvider(self):
        #variables
        selection = 0

        prov_num = input("Enter the provider's ID who's info you want to update.")
        temp_prov = self._DB.get_member(prov_num)
        print("Select Provider Field to Update\n")
        print("1. First Name")
        print("2. Last Name")
        print("3. Street Address")
        print("4. City")
        print("5. State")
        print("6. Zip Code")
        while selection < 1 or selection > 7:
            selection = input("Selection: ")
        if(selection == 1):
            temp_prov._firstName = input("Updated First Name:")
            while temp_prov._firstName is None:
                temp_prov._firstName = input("Please Enter Valid First Name:") 
        elif(selection == 2):
            temp_prov._lastName = input("Updated Last Name:")
            while temp_prov._lastName is None:
                temp_prov._lastName = input("Please Enter Valid Last Name:") 
        elif(selection == 3):
            temp_prov._streetAddress = input("Update Street Address: ")
            while temp_prov._streetAddress is None:
                temp_prov._streetAddress = input("Please Enter Valid Street Address: ")
        elif(selection == 4):
            temp_prov._city = input("Updated City: ")
            while temp_prov._city is None:
                temp_prov._city = input("Please Enter Valid City: ")     
        elif(selection == 5):
            temp_prov._state = input("Updated Two Letter State ID: ")
            while temp_prov._state is None or len(temp_prov._city) < 2:
                temp_prov._city = input("Please Enter Valid Two Letter State ID: ")
        elif(selection == 6):
            temp_prov._zipCode = input("Updated Five Digit Zipcode: ")
            while temp_prov._zipCode is None or len(temp_prov._zipCode) < 5:
                temp_prov._zipCode = input("Please Enter Valid Five Digit Zip Code: ")
        elif(selection == 7):
            temp_prov._status = input("Updated Status:")
            while temp_prov._status is None:
                temp_prov._status = input("Please Enter Valid Status")
        try:
            self._DB.update_provider(temp_prov)        
        except Exception as e:
            print(f"Error updating provider: {e}")

    #removes a provider
    def deleteProvider(self):
        prov_num = input("Enter the provider's ID who you want to delete.")
        try:
            self._DB.delete_provider(prov_num)
        except Exception as e:
            print(f"Error deleting provider: {e}")
    
    def deleteService(self):
        serv_num = input("Enter the six digit service code you wish to delete: ")
        while serv_num is None or len(serv_num) < 6 or len(serv_num) > 6:
            serv_num = input("Enter the six digit service code you wish to delete: ")
        try:
            self._DB.delete_service(serv_num)
        except Exception as e:
            print(f"Error deleting service: {e}")

    
    def addService(self):
        # Create a new Service object instead of reassigning self
        service = Service()
        
        # Get service details
        service._serviceCode = input("Six Digit Service Code:")
        while service._serviceCode is None or len(service._serviceCode) < 6 or len(service._serviceCode) > 6:
            service._serviceCode = input("Please Enter Valid Six Digit Service Code: ")
        
        service._serviceName = input("Service Name:")
        while service._serviceName is None or len(service._serviceName) > 20:
            service._serviceName = input("Please Enter a Service Name less than Twenty Characters: ")
        
        service._fee = input("Service fee:")
        while service._fee is None or len(service._fee) > 8:
            service._fee = input("Please Enter a Fee less than Eight Digits: ")
        
        try:
            # Use self._DB since this is a method of ChocAnSystem
            self._DB.insert_service(service)
        except Exception as e:
            print(f"Error adding service: {e}")
    
    #deletes a service
    def deleteService(self):
        serv_num = input("Enter the six digit service code you wish to delete: ")
        while serv_num is None or len(serv_num) < 6 or len(serv_num) > 6:
            serv_num = input("Enter the six digit service code you wish to delete: ")
        try:
            self._DB.delete_service(serv_num)
        except Exception as e:
            print(f"Error deleting service: {e}")

    def addServiceRecord(self):
        #primary key is an autoincr int
        #date_received DATETIME NOT NULL
        # service_date DATE NOT NULL
        # provider_number VARCHAR(9) NOT NULL
        # member_number VARCHAR(9) NOT NULL
        # service_code VARCHAR(6) NOT NULL
        # comments VARCHAR(100)
        # fee DECIMAL(8,2) NOT NULL
        rec = ServiceRecord()
        date_input = input("Date Record Recieved (YYYY-MM-DD): ")
        rec._dateReceived = datetime.strptime(date_input, "%Y-%m-%d")
        date_input = input("Service Date (YYYY-MM-DD): ")
        rec._serviceDate = datetime.strptime(date_input, "%Y-%m-%d")
        #rec._provider = input("Nine Digit Provider Number: ")
        #rec._member = input("Nine Digit Member Number: ")
        #rec._service = input("Six Digit Service Number: ")
        #rec._comments = input("Comments for Service Record: ")
        #rec._fee = input("Service Fee: ")
        try:
            self._DB.insert_service_record(rec)
        except Exception as e:
            print(f"Error adding service record: {e}")

    def updateServiceRecord(self):
        try:
            record_id = input("Enter the Service Record ID to update: ")
            record = self._DB.get_service_record(record_id)
            
            if not record:
                print("Service record not found.")
                return
            
            print("\nSelect field to update:")
            print("1. Service Date")
            print("2. Provider Number")
            print("3. Member Number")
            print("4. Service Code")
            print("5. Comments")
            print("6. Fee")
            
            selection = input("Selection: ")
            while not selection.isdigit() or int(selection) < 1 or int(selection) > 6:
                selection = input("Please enter a valid selection (1-6): ")
            
            selection = int(selection)
            
            if selection == 1:
                date_input = input("New Service Date (YYYY-MM-DD): ")
                record._serviceDate = datetime.strptime(date_input, "%Y-%m-%d")
            elif selection == 2:
                provider_num = input("New Provider Number (9 digits): ")
                while not re.match(r"^\d{9}$", provider_num):
                    print("Invalid provider number. Must be exactly 9 digits.")
                    provider_num = input("New Provider Number (9 digits): ")
                record._provider = provider_num
            elif selection == 3:
                member_num = input("New Member Number (9 digits): ")
                while not re.match(r"^\d{9}$", member_num):
                    print("Invalid member number. Must be exactly 9 digits.")
                    member_num = input("New Member Number (9 digits): ")
                record._member = member_num
            elif selection == 4:
                service_code = input("New Service Code (6 digits): ")
                while not re.match(r"^\d{6}$", service_code):
                    print("Invalid service code. Must be exactly 6 digits.")
                    service_code = input("New Service Code (6 digits): ")
                record._service = service_code
            elif selection == 5:
                comments = input("New Comments (max 100 characters): ")
                while len(comments) > 100:
                    print("Comments too long. Maximum 100 characters.")
                    comments = input("New Comments (max 100 characters): ")
                record._comments = comments
            elif selection == 6:
                fee = input("New Fee (max 8 digits, 2 decimal places): ")
                while not re.match(r"^\d{1,8}(\.\d{0,2})?$", fee):
                    print("Invalid fee format.")
                    fee = input("New Fee (max 8 digits, 2 decimal places): ")
                record._fee = float(fee)
                
            self._DB.update_service_record(record)
            print("Service record updated successfully.")
            
        except ValueError as e:
            print(f"Invalid input format: {e}")
        except Exception as e:
            print(f"Error updating service record: {e}")

    def deleteServiceRecord(self):
        rec_num = input("Enter the Service Record ID of the record to delete: ")
        while rec_num is None or len(rec_num) > 4096:
            print("Invalid Service Record ID")
            rec_num = input("Enter the Service Record ID of the record to delete: ")
        try:
            self._DB.delete_service_record(rec_num)
        except Exception as e:
            print(f"Error deleting service record: {e}")
             

    #updates member statuses based on payment
    def processMembershipPayments(self):
        try:
            # Get all members from database
            members = self._DB.get_all_members()
            
            print("\nProcessing membership payments...")
            for member in members:
                # Simulate payment check - in a real system this would check against actual payment records
                payment_status = input(f"\nHas member {member._memberNumber} ({member._firstName} {member._lastName}) paid? (y/n): ").lower()
                
                if payment_status == 'y':
                    if member._status != Status.VALID:
                        member._status = Status.VALID
                        self._DB.update_member(member)
                        print(f"Member {member._memberNumber} status updated to VALID")
                else:
                    if member._status != Status.SUSPENDED:
                        member._status = Status.SUSPENDED
                        self._DB.update_member(member)
                        print(f"Member {member._memberNumber} status updated to SUSPENDED")
            
            print("\nMembership payment processing complete.")
            
        except Exception as e:
            print(f"Error processing membership payments: {e}")

    #retrieves the list of services for provider
    def getProviderDirectory(self):
        provider_list = self._DB.get_provider_directory()
        for prov in provider_list:
            print(prov)
    
    def generateMemberReport(self, member_number):
        member = self._DB.get_member(member_number)
        filename = f"member_{member_number}_report.txt"
        original = sys.stdout
        with open(filename, "w") as f:
            sys.stdout = f
            print(repr(member))
            print("Services:")
            services = self._DB.get_service_records_by_member(member_number)
            for s in services:
                s.displayInfo()
        sys.stdout = original

    #creates a report for a specific provider
    def generateProviderReport(self, provider_number):
        provider = self._DB.get_provider(provider_number)
        file = "provider_" + provider_number + "_report.txt"
        original_std = sys.stdout
        with open(file, "w") as f:
            sys.stdout = f
            print(repr(provider))
            print("Services:")
            try:
                service_list = self._DB.get_service_records_by_provider()
                consultations = 0
                total_fee = 0
                for serv in service_list:
                    serv.displayInfo()
                    consultations += 1
                    total_fee += serv.fee
            except Exception as e:
                print(f"error generating provider report: {e}")
            print("")
            print(f"total consultations: {consultations}")
            print(f"total fee: {total_fee}")
        sys.stdout = original_std


    #Generates all required weekly reports
    def generateWeeklyReports(self):
        try:
            print("*** Weekly Reports:")
            print("** Provider Reports:")
            for prov in self._providers:
                self.generateProviderReport(prov._providerNumber)
            print("")
            print("Member Reports:")
            for mem in self._members:
                self.generateMemberReport(mem._memberNumber)
        except Exception as e:
            print(f"Error generating weekly reports: {e}")
