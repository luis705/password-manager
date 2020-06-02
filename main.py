import sqlite3

from os import path

from database_functions import *
from encryption_functions import get_hash, generate_key, encrypt_password, decrypt_password

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
                user_key = get_key(user_id)
                
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
                        #  Check if service isn't alredy saved
                        services_list = list_saved_services(user_id)
                        valid = False
                        while not valid:
                            service_name = input('\nWhat is the name of the service? ')
                            for service in services_list:
                                if service_name == service[0]:
                                    print("\nService alredy registered")
                                    break
                            else: valid = True

                        username = input(f"\nWhat is your username in {service_name}? ")
                        password = input(f'\nWhat is your password in {service_name}? ')
                        encrypted_password = encrypt_password(user_key, password)

                        add_service(service_name, username, encrypted_password, user_id)

                        print('\nService added successfully!')

                    elif operation == 'g':
                        service = input('\nWhat service do you want to check? ')
                        service_list = list_saved_services(user_id)

                        for existing_service in service_list:
                            if service == existing_service[0]:
                                exists = True
                                break
                        else:
                            exists = False
                        
                        if not exists:
                            print('\nThis is not a registered service')
                        else:
                            username, hashed_password = check_data_from_service(user_id, service)

                            password = decrypt_password(user_key, hashed_password)

                            print(f'\nService: {service}\nUsername: {username}\nPassword: {password}')

                    elif operation == 'u':
                        service = input('\nWhat is the service you want to update? ')

                        service_list = list_saved_services(user_id)

                        for name in service_list:
                            if name[0] == service:
                                exists = True
                                break
                        else:
                            exists = False
                        
                        if exists:
                            username = input('\nWhat will be your new username? (press enter for no changing) ')
                            password = input('\nWhat will be your new password? (press enter for no changing) ')

                            if username == '' and password == '':
                                print('\nYou must change at least one!')
                                continue
                                
                            elif username == '':

                                encrypted_password = encrypt_password(user_key, password)
                                update_service_password(user_id, service, encrypted_password)
                            
                            elif password == '':
                                update_service_username(user_id, service, username)

                            

                            elif username != '' and password != '':
                                encrypted_password = encrypt_password(user_key, password)
                                update_service_password(user_id, service, encrypted_password)
                                update_service_username(user_id, service, username)
                            
                            print('\nService updated successfully!')

                        else:
                            print("\nThis service isn't registred")

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