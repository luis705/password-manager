import sqlite3

def connect():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    return conn, cursor

def disconnect(conn):
    conn.commit()
    conn.close()

def create_database():
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
    conn, cursor = connect()

    cursor.execute('SELECT username FROM users')
    users_list = cursor.fetchall()

    disconnect(conn)

    return users_list

def add_user(username, master_hashed, key):
    conn, cursor = connect()

    cursor.execute(f'''INSERT INTO users ("username", "master_password", "key")
                    VALUES ("{username}", "{master_hashed}", "{key}")''')

    disconnect(conn)

def get_master_hashed(username):
    conn, cursor = connect()

    cursor.execute(f'SELECT master_password FROM users WHERE username="{username}"')
    master_password_hashed = cursor.fetchone()

    disconnect(conn)

    return master_password_hashed[0]

def get_user_id(username):
    conn, cursor = connect()

    cursor.execute(f'SELECT id FROM USERS WHERE username="{username}"')
    user_id = cursor.fetchone()[0]
    disconnect(conn)

    return user_id

def delete_user(user_id):
    conn, cursor = connect()

    cursor.execute(f'DELETE FROM users WHERE id={user_id}')
    cursor.execute(f'DELETE FROM services WHERE user_id={user_id}')

    disconnect(conn)

def list_saved_services(user_id):
    conn, cursor = connect()

    cursor.execute(f'SELECT service_name FROM services WHERE user_id="{user_id}"')
    services = cursor.fetchall()
    disconnect(conn)

    return services

def get_key(user_id):
    conn, cursor = connect()

    cursor.execute(f'SELECT key FROM users where id="{user_id}"')
    key = cursor.fetchone()[0]
    key = key[2:-1]
    disconnect(conn)

    return key.encode()

def add_service(service_name, username, encrypted_password, user_id):
    conn, cursor = connect()

    cursor.execute(f'''
                    INSERT INTO services (service_name, username, password, user_id)
                    VALUES ("{service_name}", "{username}", "{encrypted_password}", "{user_id}")''')
    disconnect(conn)

def check_data_from_service(user_id, service_name):
    conn, cursor = connect()

    cursor.execute(f'''
                    SELECT username, password
                    FROM services
                    WHERE user_id="{user_id}"
                    AND service_name="{service_name}"
                    ''')

    results = cursor.fetchone()
    disconnect(conn)

    return results[0], results[1][2:-1]

def update_service_username(user_id, service, username):
    conn, cursor = connect()
    
    cursor.execute(f'''
                    UPDATE services
                    SET username="{username}"
                    WHERE user_id="{user_id}"
                    AND service_name="{service}"''')
    disconnect(conn)

def update_service_password(user_id, service, password):
    conn, cursor = connect()
    
    cursor.execute(f'''
                    UPDATE services
                    SET password="{password}"
                    WHERE user_id="{user_id}"
                    AND service_name="{service}"''')
    disconnect(conn)

def delete_service(user_id, service):
    conn, cursor = connect()

    cursor.execute(f'DELETE FROM services WHERE user_id="{user_id}" AND service_name="{service}"')
    disconnect(conn)
