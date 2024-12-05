from enum import Enum
from datetime import date
import os               # File IO
import re               # Regex (idx might come in handy, it's good to have too many then too little)
import logging          # Nice interface for logging, just captures timestamp and formats nice
from dataclasses import dataclass, field # Class helpers, py 3.8+ features that make classes much shorter to write
from typing import *    # Type hinting
import sys

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

    #initializes a new service record
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
        pass

class ChocAnSystem:
    def __init__(self) -> None:
        #list of members objects
        self._members = None
        #list of Provider objects
        self._providers = None
        #list of service objects
        self._services = None
        #list of service Record objects
        self._serviceRecords = None

        #import Database manager locally to not get
        #circular depencies
        from database import DatabaseManager
        self._DB = DatabaseManager("chocoDB")
        pass

    # print validated if member id is found
    # print Invalid if member id is not found or suspended
    # return valid id or 0 if invalid
    def validateMember(self):
        pass

    def validateProvider(self):
        pass

    def addMember(self):
        mem = Member()
        #member_number VARCHAR(9) PRIMARY KEY,
        mem._memberNumber = input("Nine Digit Member Number: ")
        while mem._memberNumber is None or len(mem._memberNumber) < 9:
            mem._memberNumber = input("Please Enter Valid Nine Digit Member Number: ")

        #first_name VARCHAR(25) NOT NULL,
        mem._firstName = input("First Name:")
        while mem._firstName is None:
            mem._firstName = input("Please Enter Valid First Name:")

        #last_name VARCHAR(25) NOT NULL,
        mem._lastName = input("Last Name:")
        while mem._lastName is None:
            mem._lastName = input("Please Enter Valid Last Name:")

        #street_address VARCHAR(25),
        mem._streetAddress = input("Street Address: ")
        while mem._streetAddress is None:
            mem._streetAddress = input("Please Enter Valid Street Address: ")

        #city VARCHAR(14),
        mem._city = input("City: ")
        while mem._city is None:
            mem._city = input("Please Enter Valid City: ")
        #state VARCHAR(2),
        mem._state = input("Two Letter State ID: ")
        while mem._state is None or len(mem._city) < 2:
            mem._city = input("Please Enter Valid Two Letter State ID: ")
        #zipcode VARCHAR(5),
        mem._zipCode = input("Five Digit Zipcode: ")
        while mem._zipCode is None or len(mem._zipCode) < 5:
            mem._zipCode = input("Please Enter Valid Five Digit Zip Code: ")
        #status TEXT CHECK(status IN ('VALID', 'SUSPENDED', 'INVALID')) NOT NULL DEFAULT 'VALID'
        self._DB.insert_member(mem)
        pass
    
    #updates member information
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
        self._DB.update_member(member)        
        pass

    def deleteMember(self):
        mem_num = input("Please Enter Member Number to Delete: ")
        self._DB.delete_member(mem_num)
        pass

    #adds new provider
    def addProvider(self):
        
        #get provider info
        f_name = input("Enter the first name of the provider")
        while not re.match(r"^[a-zA-Z]+$",f_name):
            print("Invalid first name. Only letter are allowed.")
            f_name = input("Enter the first name of the provider")
            
        l_name = input("Enter the last name of the provider")
        while not re.match(r"^[a-zA-Z]+$",f_name):
            print("Invalid first name. Only letter are allowed.")
            l_name = input("Enter the last name of the provider")

        p_str_addr = input("Enter the street address of provider")
        while not re.match(r"^[a-zA-Z0-9\s,.#-]+$", p_str_addr):
            print("Invalid address. Only letters, numbers, and common address symbols (.,#-) are allowed.")
            p_str_addr = input("Enter the street address of provider: ")

        city = input("Enter the city of provider")
        while not re.match(r"^[a-zA-Z\s]+$", city):
            print("Invalid city. Only letters and spaces are allowed.")
            city = input("Enter the city of provider: ")

        st = input("Enter the state of the provider")
        while not re.match(r"^[A-Z]{2}$", st):
            print("Invalid state. Enter exactly two uppercase letters (e.g., 'CA').")
            st = input("Enter the state of the provider (e.g., 'CA'): ")


        zip = input("Enter the zipcode of provider")
        while not re.match(r"^\d{5}$", zip):
            print("Invalid ZIP code. Enter exactly 5 digits.")
            zip = input("Enter the zipcode of provider: ")

        #make a new Provider object
        new_provider = Provider(f_name,l_name,p_str_addr,city,st,zip)
        self._DB.insert_provider(new_provider)

    #updates provider information
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
        self._DB.update_provider(temp_prov)        
        pass

    #removes a provider
    def deleteProvider(self):
        prov_num = input("Enter the provider's ID who you want to delete.")
        self._DB.delete_provider(prov_num)
        pass

    def addService(self):
        self = Service()
        #service_code VARCHAR(6) PRIMARY KEY
        self._serviceCode = input("Six Digit Service Code:")
        while self._serviceCode is None or len(self._serviceCode) < 6:
            self._serviceCode = input("Please Enter Valid Six Digit Service Code: ")
        #service_name VARCHAR(20) 
        self._serviceName = input("Service Name:")
        while self._serviceName is None or len(self._serviceName) < 20:
            self._serviceName = input("Please Enter a Service Name less than Twenty Characters: ")
        #fee DECIMAL(8,2)
        self._fee = input("Service Fee:")
        while self._fee is None or len(self._fee) < 8:
            self._fee = input("Please Enter a Fee less than Eight Digits: ")
        self._DB.add_service(self)
        pass
    
    def deleteService(self):
        serv_num = input("Enter the six digit service code you wish to delete: ")
        while serv_num is None or len(serv_num) < 6:
            serv_num = input("Enter the six digit service code you wish to delete: ")
        self._DB.delete_service(serv_num)

    
    #adds a new service record
    def addServiceRecord(self):
        self = Service()
        #service_code VARCHAR(6) PRIMARY KEY
        self._serviceCode = input("Six Digit Service Code:")
        while self._serviceCode is None or len(self._serviceCode) < 6:
            self._serviceCode = input("Please Enter Valid Six Digit Service Code: ")
        #service_name VARCHAR(20) 
        self._serviceName = input("Service Name:")
        while self._serviceName is None or len(self._serviceName) < 20:
            self._serviceName = input("Please Enter a Service Name less than Twenty Characters: ")
        #fee DECIMAL(8,2)
        self._fee = input("Service Name:")
        while self._fee is None or len(self._fee) < 8:
            self._fee = input("Please Enter a Fee less than Eight Digits: ")
        pass
    
    #deletes a service
    def deleteService(self):
        serv_num = input("Enter the six digit service code you wish to delete: ")
        while serv_num is None or len(serv_num) < 6:
            serv_num = input("Enter the six digit service code you wish to delete: ")
        self._DB.delete_service(serv_num)

    #updates member statuses based on payment
    def processMembershipPayments(self):
        pass

    #retrieves the list of services for provider
    def getProviderDirectory(self):
        pass
    
    #creates a report for a specific member
    def generateMemberReport(self, member_number):
        member = self._DB.get_member(member_number)

        file = "member_" + member_number + "_report.txt"
        with open(file, "w") as f:
            original_std = sys.stdout
            sys.stdout = f

            print(member.__repr__)
            print("Services:")
            service_list = self._DB.get_service_records_by_member()
            for serv in service_list:
                serv.displayInfo()
        sys.stdout = original_std
        f.close()



    #creates a report for a specific provider
    def generateProviderReport(self, provider_number):
        provider = self._DB.get_provider(provider_number)
        file = "provider_" + member_number + "_report.txt"
        with open(file, "w") as f:
            original_std = sys.stdout
            sys.stdout = f

            print(provider.__repr__)
            print("Services:")
            service_list = self._DB.get_service_records_by_provider()
            consultations = 0
            total_fee = 0
            for serv in service_list:
                serv.displayInfo()
                consultations += 1
                total_fee = total_fee + serv.fee
            print("")
            print("Total consulations:" + consultations)
            print("Total fee:" + total_fee)
        sys.stdout = original_std
        f.close()


    #Generates all required weekly reports
    def generateWeeklyReports(self):
        print("*** Weekly Reports:")
        print("** Provider Reports:")
        for prov in self._providers:
            self.generateProviderReport(prov._providerNumber)
        print("")
        print("Member Reports:")
        for mem in self._members:
            self.generateMemberReport(mem._memberNumber)