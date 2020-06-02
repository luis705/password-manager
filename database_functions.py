import sqlite3

def create_database():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()

def get_usernames_list():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()

    cursor.execute('SELECT username FROM users')
    users_list = cursor.fetchall()

    conn.commit()
    conn.close()

    return users_list

def add_user(username, master_hashed, key):

    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()

    cursor.execute(f'''INSERT INTO users ("username", "master_password", "key")
                    VALUES ("{username}", "{master_hashed}", "{key}")''')

    conn.commit()
    conn.close()

def get_master_hashed(username):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT master_password FROM users WHERE username="{username}"')
    master_password_hashed = cursor.fetchone()

    conn.commit()
    conn.close()

    return master_password_hashed[0]

def get_user_id(username):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT id FROM USERS WHERE username="{username}"')
    user_id = cursor.fetchone()[0]
    return user_id

def delete_user(user_id):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()

    cursor.execute(f'DELETE FROM users WHERE id={user_id}')
    cursor.execute(f'DELETE FROM services WHERE user_id={user_id}')

    conn.commit()
    conn.close()