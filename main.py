import sqlite3

from os import path

from database_functions import create_database, get_usernames_list, add_user, get_master_hashed, delete_user, get_user_id, list_saved_services
from encryption_functions import get_hash, generate_key

def main_menu():
    print('------------------------------')
    print('|   What do you want to do?  |')
    print('| "l": login                 |')
    print('| "s": sign up               |')
    print('| "d": delete user           |')
    print('| "e": exit                  |')
    print('------------------------------')
    return input()

def user_menu():
    print('-----------------------------------------')
    print('|       What do you want to do?         |')
    print('| "l": list saved services              |')
    print('| "a": add new service                  |')
    print('| "g": get data from a service          |')
    print('| "u": update data from a service       |')
    print('| "d": delete a service                 |')
    print('| "e": exit                             |')
    print('-----------------------------------------')
    return input()

def check_user(username, provided_hash):
    user_exist = False
    users_list = get_usernames_list()
    
    for user in users_list:
        if username == user[0]:
            if provided_hash == get_master_hashed(username):
                return True
                break
            else:
                return False
                break
    else:
        return None

def main():
    if not path.exists('passwords.db'):
        create_database()
    

    while True:
        option = main_menu()

        if option not in ['l', 's', 'd', 'e']:
            print('Invalid option\n')
        
        elif option == 'e':
            exit()
        
        elif option == 's':
            #  Create new user
            print('I will need some informations. DO NOT FORGET OR YOU WILL LOSE ACCESS TO ALL YOUR PASSWORDS\n')
            
            #  Check if username is valid
            users_list = get_usernames_list()
            valid = False
            while not valid:
                username = input('\nWhat is your username? ')
                for name in users_list:
                    if username == name[0]:
                        print('\nUsername alredy taken')
                        break
                else:
                    valid = True
            
            master_password = input('\nWhat is your master password? ')
            master_hashed = get_hash(master_password)
            key = generate_key()

            #try:
            add_user(username, master_hashed, key)
            print('\nUser added successully!')
            #except sqlite3.Error:
                #print('\nAn error ocurred, try again later')

        elif option == 'l':
            username = input('\nWhat is your username? ')
            provided_password = input('\nWhat is your master password? ')
            provided_hashed = str(get_hash(provided_password))

            accessed = check_user(username, provided_hashed)

            if accessed == True:
                print(f'\nWellcome {username}\n')
                user_id = get_user_id(username)
                
                while True:
                    operation = user_menu()

                    if operation not in ['l', 'a', 'g', 'u', 'd', 'e']:
                        print('\nInvalid option!')
                    
                    elif operation == 'e':
                        print(f'\nGoodbye {username}!\n')
                        break
            
                    elif operation == 'l':
                        services_list = list_saved_services(user_id)

                        if len(services_list) == 0:
                            print("\nThere are no services yet\n")
                        else:
                            print('\nOkay, listing services...\n')
                            for i in range(len(services_list)):
                                print(f'Service {i + 1}: {services_list[i][0]}\n')

                    elif operation == 'a':
                        pass

                    elif operation == 'g':
                        pass

                    elif operation == 'u':
                        pass

                    elif operation == 'd':
                        pass

            elif accessed == False:
                print('\nAccess denied!')
            
            elif accessed == None:
                print('\nUser not found')
        
        elif option == 'd':
            username = input('\nWhat is your username? ')
            provided_password = input('\nWhat is your master password? ')
            provided_hashed = str(get_hash(provided_password))

            accessed = check_user(username, provided_hashed)

            if accessed == True:
                user_id = get_user_id(username)
                delete_user(user_id)
                print(f'\nThe user {username} was deleted successfully')
            
            elif accessed == False:
                print('\nAccess denied!')
            
            elif accessed == None:
                print("\nThis user doesn't exists")


if __name__ == "__main__":
    main()