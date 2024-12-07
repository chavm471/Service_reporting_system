from database import *
from classes import *

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
            print("0: Return to main menu\n\n")
            option = self.get_option(0, 5)

            if option == 1:
                member_number = input("Enter member number: ")
                if self._chocsystem.validateMember(member_number):
                    print("Member is valid")
                else:
                    print("Member is invalid")
            if option == 2:
                try:
                    self._chocsystem.addServiceRecord()
                except Exception as e:
                    print(f"Error logging service: {e}")
            if option == 3:
                try:
                    self._chocsystem.getProviderDirectory()
                except Exception as e:
                    print(f"Error getting provider directory: {e}")
                pass
            if option == 4:
                try:
                    self._chocsystem.addService()
                except Exception as e:
                    print(f"Error adding service: {e}")
                pass
            if option == 5:
                try:
                    self._chocsystem.deleteService()
                except Exception as e:
                    print(f"Error deleting service: {e}")
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
            print("0: Return to main menu\n\n")
            option = self.get_option(0, 9)

            if option == 1: 
                self._chocsystem.addMember()
            if option == 2:
                self._chocsystem.deleteMember()
            if option == 3:
                self._chocsystem.updateMember()
            if option == 4:
                self._chocsystem.addProvider()
            if option == 5:
                self._chocsystem.deleteProvider()
            if option == 6:
                self._chocsystem.updateProvider()
            if option == 7:
                self._chocsystem.addService()
            if option == 8:
                self._chocsystem.deleteService()
            if option == 9:
                self._chocsystem.generateWeeklyReports()

        return
