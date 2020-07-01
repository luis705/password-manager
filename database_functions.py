import sqlite3


def connect():
    """Create a connection to the sqlite database"""
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    return conn, cursor


def disconnect(conn):
    """Destroy the connection to the sqlite database"""
    conn.commit()
    conn.close()


def create_database():
    """Create the passwords ans users database if it doesn't exists"""
    conn, cursor = connect()

    cursor.execute('''
        CREATE TABLE "users" (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "username" TEXT NOT NULL,
        "master_password" BLOB NOT NULL,
        "key" BLOB NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE "services" (
        "service_name" TEXT NOT NULL,
        "username" TEXT NOT NULL,
        "password" BLOB NOT NULL,
        "user_id" INT NOT NULL,
        CONSTRAINT fk_users
        FOREIGN KEY ("user_id")
        REFERENCES users(id)
        );
    ''')

    disconnect(conn)


def get_usernames_list():
    """SQL query to get the list of usernames"""
    conn, cursor = connect()

    cursor.execute('SELECT username FROM users')
    users_list = cursor.fetchall()

    disconnect(conn)

    return users_list


def add_user(username, master_hashed, key):
    """
    SQL query to add new user into users table

    Parameters:
      username (string): username of the new user
      master_hashed (bytestring): hash of the password of the new user
      key (bytestring): key to encrypt and decrypt the new user passwords

    """
    conn, cursor = connect()

    cursor.execute(f'''INSERT INTO users ("username", "master_password", "key")
                    VALUES ("{username}", "{master_hashed}", "{key}")''')

    disconnect(conn)


def get_master_hashed(username):
    """
    SQL query to retrive master password of a given user

    Parameters:
      username(string): name of the user wich master password is required

    Returns:
      master_password_hashed[0] (bytestring): hash of the user's master password

    """
    conn, cursor = connect()

    cursor.execute(f'SELECT master_password FROM users WHERE username="{username}"')
    master_password_hashed = cursor.fetchone()

    disconnect(conn)

    return master_password_hashed[0]


def get_user_id(username):
    """
    SQL query to retrieve id of a given user

    Parameters:
      username(string): name of the user wich id password is required

    Returns:
      user_id (integer): id of the user

    """
    conn, cursor = connect()

    cursor.execute(f'SELECT id FROM USERS WHERE username="{username}"')
    user_id = cursor.fetchone()[0]
    disconnect(conn)

    return user_id


def delete_user(user_id):
    """
    SQL query to delete a given user

    Parameters:
      user_id(integer): id of the user to be deleted

    """
    conn, cursor = connect()

    cursor.execute(f'DELETE FROM users WHERE id={user_id}')
    cursor.execute(f'DELETE FROM services WHERE user_id={user_id}')

    disconnect(conn)


def list_saved_services(user_id):
    """
    SQL query to retrieve all services from a given user

    Parameters:
      user_id(integer): id of the user wich services are required

    Returns:
      services (list): list of services names

    """
    conn, cursor = connect()

    cursor.execute(f'SELECT service_name FROM services WHERE user_id="{user_id}"')
    services = cursor.fetchall()
    disconnect(conn)

    return services


def get_key(user_id):
    """
    Get encryption key of the given user

    Parameters:
      user_id(integer): id of the user wich key is required

    Returns:
      key (bytestring): encryption key of the user
    """
    conn, cursor = connect()

    cursor.execute(f'SELECT key FROM users where id="{user_id}"')
    key = cursor.fetchone()[0]
    key = key[2:]
    disconnect(conn)

    return key.encode()


def add_service(service_name, username, encrypted_password, user_id):
    """
    SQL query to add a service to the services database

    Parameters
      service_name (string): name of the service to be added
      username (string): username of user on service to be added
      encrypted_password (bytestring): encrypted password of user on service to be added
      user_id (integer): id of the user

    """
    conn, cursor = connect()

    cursor.execute(f'''
                    INSERT INTO services (service_name, username, password, user_id)
                    VALUES ("{service_name}", "{username}", "{encrypted_password}", "{user_id}")''')
    disconnect(conn)


def check_data_from_service(user_id, service_name):
    """
    SQL query to retrieve data from a service from the services database

    Parameters:
      user_id (integer): id of the user
      service_name (string): name of the service to be checked

    Returns:
      results[0] (string): username on the given service
      results[1][2:] (bytestring): encrypted password on the given service
    """
    conn, cursor = connect()

    cursor.execute(f'''
                    SELECT username, password
                    FROM services
                    WHERE user_id="{user_id}"
                    AND service_name="{service_name}"
                    ''')

    results = cursor.fetchone()
    disconnect(conn)

    return results[0], results[1][2:]


def update_service_username(user_id, service, username):
    """
    SQL query to update the username of a service in the services database

    Parameters:
      user_id (integer): id of the user updating the username
      service (string): name of the service to be updated
      username (string): new username on the service

    """
    conn, cursor = connect()

    cursor.execute(f'''
                    UPDATE services
                    SET username="{username}"
                    WHERE user_id="{user_id}"
                    AND service_name="{service}"''')
    disconnect(conn)


def update_service_password(user_id, service, password):
    """
    SQL query to update the password of a service in the services database

    Parameters:
      user_id (integer): id of the user updating the username
      service (string): name of the service to be updated
      password (string): new encrypted password on the service

    """
    conn, cursor = connect()

    cursor.execute(f'''
                    UPDATE services
                    SET password="{password}"
                    WHERE user_id="{user_id}"
                    AND service_name="{service}"''')
    disconnect(conn)


def delete_service(user_id, service):
    """
    SQL querry to delete a given service from the services database

    Parameters:
      user_id (integer): id of the user to have a service deleted
      service (string): name of the service to be deleted
    """
    conn, cursor = connect()

    cursor.execute(f'DELETE FROM services WHERE user_id="{user_id}" AND service_name="{service}"')
    disconnect(conn)
