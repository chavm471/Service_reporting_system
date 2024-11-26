from database import *

class MenuController:
    def __init__(self) -> None:
        self.provider_menu = ProviderMenu()
        self.manager_menu = ManagerMenu()
        pass

    def startmenu(self):
        print("select what mode you want")
        print("0.Manager mode")
        print("1.Provider Mode")
        mode:int = input()

        #check if its manager or provider
        if mode == 1:
            #show provide
            member_num = input("enter you membership number")
        else:
            self.manager_menu._db.get_provider(member_num)
            #show manager
            self.manager_menu(self)
            pass


        #go either into manager menu

        #or provider menu

class ProviderMenu():
    def __init__(self) -> None:
        pass

    def prompt_provider_menu(self):
        pass


class ManagerMenu():
    def __init__(self) -> None:
        self._choco = ChocAnSystem()
        pass

    def prompt_manager_menu(self):
        selection:int = None
        print("Manager Menu")
        print("1. Add Member")
        print("2. Remove Member")
        print("3. Update Member")
        print("4. Add Provider")
        print("5. Update Provider")
        print("6. Remove Provider")
        print("7. Add Service")
        print("8. Remove Service")
        print("9. Weekly reports")
        selection = input("Enter option:")
        while not re.match(r"^\d{1}$", selection):
            print("Invalid option. Enter exactly 1 digit")
            selection = input("Enter option:")

        #add provider
        if(selection == 4):
            #call the insert provider function from chocansystem class
            self._choco.addProvider()
            pass

        #update provider
        if(selection == 5):
            self._choco.updateProvider()
            pass

        #remove provider
        if(selection == 6):
            #call the remove provider from chocansystem class
            self._choco.deleteProvider()
            pass
