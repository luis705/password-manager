from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

def get_hash(string):

    byte_string = string.encode()

    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(byte_string)

    hashed_string = digest.finalize()
    return hashed_string

def generate_key():
    return Fernet.generate_key()

def encrypt_password(key, password):
    f = Fernet(key)
    token = f.encrypt(password.encode())
    return token

def decrypt_password(key, encrypted_password):
    f = Fernet(key)
    password = f.decrypt(encrypted_password.encode())
    return password.decode()
