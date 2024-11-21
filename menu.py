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
        mode = input()

        #check if its manager or provider
        if mode:
            #show provide
            member_num = input("enter you membership number")
        else:
            #show manager
            pass


        #go either into manager menu

        #or provider menu

class ProviderMenu():
    def __init__(self,db_manager) -> None:
        self._db = db_manager
        self._provider = None
        pass

    def prompt_provider_menu(self):
        input:int = None
        print("Provider Menu")
        print("1.")
        print("2.")
        print("3.")
        print("4. Add Provider")
        print("5. Update Provider")
        print("6. Remove Provider")
        print("7.")


        #add provider
        if(input == 4):
            #get provider info
            f_name = input("Enter the first name of the provider")
            l_name = input("Enter the last name of the provider")
            p_str_addr = input("Enter the street address of provider")
            city = input("Enter the city of provider")
            st = input("Enter the state of the provider")
            zip = input("Enter the zipcode of provider")

            #make a new Provider object
            new_provider = Provider(f_name,l_name,p_str_addr,city,st,zip)
            self._db.insert_provider(new_provider)
            pass

        #update provider
        if(input == 5):
            update_prov = input("Enter the provider's ID who's info you want to update.")
            self._db.update_provider(update_prov)
            pass

        #remove provider
        if(input == 6):
            remove_prov = input("Enter the provider's ID who you want to delete.")
            self._db.remove_provider(remove_prov)
            pass

        pass


class ManagerMenu():
    def __init__(self,db_manager) -> None:
        self._db = db_manager
        pass
