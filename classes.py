from enum import Enum
from datetime import date

class Status(Enum):
    VALID = 1
    SUSPENDED = 2
    INVALID = 3

class Member:
    #constructor
    def __init__(self) -> None:
        self._memberNumber:str = None
        self._firstName:str = None
        self._lastName:str = None
        self._streetAddress:str = None
        self._city:str = None
        self._state:str = None
        self._zipCode:str = None
        self._status: Status = Status.INVALID
    
    #validate function checks if the members status
    #allows them to receive services
    def validate(self):
        pass
    
    #updates the members status
    def updateStatus(self,newStatus):
        pass
    
    #displays member information
    def displayInfo(self):
        print("Member Number:",self._memberNumber)
        print("First Name:",self._firstName)
        print("Last Name",self._lastName)
        print("Address:",self._streetAddress,self._city,self._state,self._zipCode)
        print("Membership Status:",self._status)
        pass

class Provider:
    def __init__(self) -> None:
        self._providerNumber:str = None
        self._name:str = None
        self._streetAddress:str = None
        self._city:str = None
        self._state:str = None
        self._zipCode:str = None
        pass

    #methods

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

    def displayInfo(self):
        print("Provider Number:",self._providerNumber)
        print("Name:",self._name)
        print("Address:",self._streetAddress,self._city,self._state,self._zipCode)
        pass

class Service:
    def __init__(self) -> None:
        self._serviceCode:str = None
        self._serviceName:str = None
        self._fee:float = None
        pass

    #show service details
    def displayInfo(self):
        print("Service Name:",self._serviceName)
        print("Service Code:",self._serviceCode)
        print("Fee:",self._fee)
        pass

class ServiceRecord:
    def __init__(self) -> None:
        self._recordID:int = None
        self._dateReceived = date.today()
        #i just put that date for now
        self._serviceDate = date(2023, 10, 21)
        self._provider = None
        self._member = None
        self._service = None
        self._comments = None
        self._fee = None
        pass

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
        pass

    def validateMember(self):
        pass

    def validateProvider(self):
        pass

    def addMember(self):
        pass
    
    #updates member information
    def updateMember(self):
        pass

    def deleteMember(self):
        pass

    #adds new provider
    def addProvider(self):
        pass

    #updates provider information
    def updateProvider(self):
        pass

    #removes a provider
    def deleteProvider(self):
        pass
    
    #adds a new service record
    def addServiceRecord(self):
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