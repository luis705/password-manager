from os import path

from database_functions import create_database

def main_menu():
    print('-----------------------------------------')
    print('|   What do you want to do?             |')
    print('| "l": list saved services              |')
    print('| "a": add new service                  |')
    print('| "g": get data from a service          |')
    print('| "u": update data from a service       |')
    print('| "d": delete a service                 |')
    print('| "e": exit                             |')
    print('-----------------------------------------')
    
    return input()

def main():
    if not path.exists('passwords.db'):
        create_database()
    

    while True:
        option = main_menu()

        if option not in ['l', 's', 'd', 'e']:
            print('Invalid option\n')
        
        elif option == 'e':
            exit()

        elif option == 'l':
            pass

        elif option == 's':
            pass

        elif option == 'd':
            pass

