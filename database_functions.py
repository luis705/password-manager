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

    print(username, type(username))
    print(master_hashed, type(master_hashed))
    print(key, type(key))

    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()

    cursor.execute(f'''INSERT INTO users ("username", "master_password", "key")
                    VALUES ("{username}", "{master_hashed}", "{key}")''')

    conn.commit()
    conn.close()
