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
        print("░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█��▒░\n") 
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
                    # Get provider number
                    provider_number = input("Enter provider number: ")
                    provider = self._chocsystem._DB.get_provider(provider_number)
                    if provider:
                        # Create and record service
                        service_record = ServiceRecord()
                        service_record.createRecord()
                        provider.recordService(service_record)
                        print("Service recorded successfully")
                    else:
                        print("Provider not found")
                except Exception as e:
                    print(f"Error logging service: {e}")
            if option == 3:
                try:
                    provider_number = input("Enter provider number: ")
                    provider = self._chocsystem._DB.get_provider(provider_number)
                    if provider:
                        provider.requestProviderDirectory()
                    else:
                        print("Provider not found")
                except Exception as e:
                    print(f"Error getting provider directory: {e}")
            if option == 4:
                try:
                    service = Service()
                    # Service details will be prompted within addService
                    self._chocsystem.addService()
                except Exception as e:
                    print(f"Error adding service: {e}")
            if option == 5:
                try:
                    self._chocsystem.deleteService()
                except Exception as e:
                    print(f"Error deleting service: {e}")

    def manager_options(self) -> None:
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
            print("9: Generate weekly reports\n")
            print("0: Return to main menu\n\n")
            option = self.get_option(0, 9)

            try:
                if option == 1: 
                    # Use the prompt_member_constructor for adding new members
                    new_member = Member.prompt_member_constructor()
                    self._chocsystem._DB.insert_member(new_member)
                    print("Member added successfully")
                elif option == 2:
                    self._chocsystem.deleteMember()
                elif option == 3:
                    self._chocsystem.updateMember()
                elif option == 4:
                    # Use the prompt_provider_constructor for adding new providers
                    new_provider = Provider.prompt_provider_constructor()
                    self._chocsystem._DB.insert_provider(new_provider)
                    print("Provider added successfully")
                elif option == 5:
                    self._chocsystem.deleteProvider()
                elif option == 6:
                    self._chocsystem.updateProvider()
                elif option == 7:
                    self._chocsystem.addService()
                elif option == 8:
                    self._chocsystem.deleteService()
                elif option == 9:
                    self._chocsystem.generateWeeklyReports()
            except Exception as e:
                print(f"Error performing operation: {e}")
