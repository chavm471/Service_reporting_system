from database import *
from classes import *

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
            self.provider_menu.prompt_provider_menu()
        else:
            self.manager_menu.prompt_manager_menu()
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

class Menu:
    def __init__ (self) -> None:
        self._chocsystem = ChocAnSystem()

    def startup(self) -> None:
        # show chocan logo
        print(" ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ \n")
        print("░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░\n") 
        print("░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░\n") 
        print("░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░\n") 
        print("░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░\n") 
        print("░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░\n") 
        print(" ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░\n\n")

    def get_option(self, low: int, high: int) -> int:
        # get an option wihin the valid range and
        # return if valid int
        if (low > high or high < low):
            return -999
        option: int
        while (True):
            try:
                option = int(input("Enter selection: "))
            except ValueError:
                print("Invalid Input: Please enter a number")
                continue
            if option < low or option > high:
                print("Invalid Input: Choose an option between ", low, " and ", high)
                continue
            else:
                break

        return option

    def main_menu(self) -> None:
        option: int = 999

        while option != 0:
            print("1: Enter manager mode\n")
            print("2: Enter provider mode\n")
            print("0: Close the terminal\n\n")
            option = self.get_option(0, 2)

            if option == 1:
                self.manager_options()

            if option == 2:
                # need to write section to validate provider info 
                self.provider_options()

        print("Thank you for using ChocAn!")


    def provider_options(self) -> None:
        # print prover menu and call provider methods
        option: int = 999
        
        while option != 0:
            print("1: Validate member\n")
            print("2: Log service for member\n")
            print("3: Get provider directory\n")
            print("4: Add service provided\n")
            print("5: Remove service provided\n")
            print("0: Close the terminal\n\n")
            option = self.get_option(0, 5)

            if option == 1:
                pass
            if option == 2:
                pass
            if option == 3:
                pass
            if option == 4:
                pass
            if option == 5:
                pass

        return
        

    def manager_options(self) -> None:
        # print manager menu and call provider options
        option: int = 999
        
        while option != 0:
            print("1: Add member\n")
            print("2: Remove member\n")
            print("3: Update member\n")
            print("4: Add provider\n")
            print("5: Remove provider\n")
            print("6: Update provider\n")
            print("7: Add service\n")
            print("8: Remove service\n")
            print("9: Get weekly reports\n")
            print("0: Close the terminal\n\n")
            option = self.get_option(0, 9)

            if option == 1:
                pass
            if option == 2:
                pass
            if option == 3:
                pass
            if option == 4:
                pass
            if option == 5:
                pass
            if option == 6:
                pass
            if option == 7:
                pass
            if option == 8:
                pass
            if option == 9:
                pass

        return
