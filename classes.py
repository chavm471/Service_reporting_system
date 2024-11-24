from enum import Enum
from datetime import date
import os               # File IO
import re               # Regex (idx might come in handy, it's good to have too many then too little)
import logging          # Nice interface for logging, just captures timestamp and formats nice
from dataclasses import dataclass, field # Class helpers, py 3.8+ features that make classes much shorter to write
from typing import *    # Type hinting
from database import DatabaseManager

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
        self._DB = DatabaseManager()
        pass

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
        print("Five Digit ZipCode: ")
        mem._zipCode = input("Five Digit Zipcode: ")
        while mem._zipCode is None or len(mem._zipCode) < 5:
            mem._zipCode = input("Please Enter Valid Five Digit Zip Code: ")
        #status TEXT CHECK(status IN ('VALID', 'SUSPENDED', 'INVALID')) NOT NULL DEFAULT 'VALID'
        self._DB.insert_member(mem)
        pass
    
    #updates member information
    def updateMember(self):
        pass

    def deleteMember(self):
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
        city = input("Enter the city of provider")
        st = input("Enter the state of the provider")
        zip = input("Enter the zipcode of provider")

        #make a new Provider object
        new_provider = Provider(f_name,l_name,p_str_addr,city,st,zip)
        self._DB.insert_provider(new_provider)
        pass

    #updates provider information
    def updateProvider(self):
        prov_num = input("Enter the provider's ID who's info you want to update.")
        self._DB.update_provider(prov_num)
        pass

    #removes a provider
    def deleteProvider(self):
        prov_num = input("Enter the provider's ID who you want to delete.")
        self._DB.delete_provider(prov_num)
        pass
    
    #adds a new service record
    def addServiceRecord(self):
        #Test Comment, Marc added
        pass

    #Generates all required weekly reports
    def generateWeeklyReports(self):
        pass

    #updates member statuses based on payment
    def processMembershipPayments(self):
        pass

    #retrieves the list of services for provider
    def getProviderDirectory(self):
        pass

class ReportGenerator:
    def __init__(self) -> None:
        pass

    #creates a report for a specific member
    def generateMemberReport(self):
        pass

    #creates a report for a specific provider
    def generateProviderReport(self):
        pass

    #generates eft data for provider payments
    def generateEFTData(self):
        pass

    #creates the provider directory file
    def generateProviderDirectory(self):
        pass
