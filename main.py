import sqlite3

from os import path

from database_functions import create_database, get_usernames_list, add_user, get_master_hashed, delete_user, get_user_id
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
            pass

        elif option == 'd':
            username = input('\nWhat is your username? ')
            provided_password = input('\nWhat is your master password? ')
            provided_hashed = str(get_hash(provided_password))

            user_exist = False
            users_list = get_usernames_list()
            for user in users_list:
                if username == user[0]:
                    user_exist = True
                    break
            else:
                print("\nThis user doesn't exists")
            
            if user_exist:
                master_hashed = get_master_hashed(username)

                if provided_hashed == master_hashed:
                    user_id = get_user_id(username)
                    delete_user(user_id)
                    print(f'\nThe user {username} was deleted successfully')
                
                else:
                    print('\nAccess denied!')




if __name__ == "__main__":
    main()