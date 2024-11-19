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
    
    """updates the members status
    """
    def updateStatus(newStatus):
        pass
    
    #displays member information
    def displayInfo():
        pass

class Provider:
    def __init__(self) -> None:
        self._providerNumber:str = None
        self._name:str = None
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

        pass

class Service:
    def __init__(self) -> None:
        self._serviceCode:str = None
        self._serviceName:str = None
        self._fee:float = None
        pass

    #show service details
    def displayInfo(self):
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

        pass