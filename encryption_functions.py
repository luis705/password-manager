from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


def get_hash(string):
    """
    Returns a hash from a string

    Parameters:
      string (str): the string used to generate the hash

    Returns:
      hash(string): the hash of the string
    """

    byte_string = string.encode()

    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(byte_string)

    hashed_string = digest.finalize()
    return hashed_string


def generate_key():
    """Create key to encrypt and decrypt passwords"""
    return Fernet.generate_key()


def encrypt_password(key, password):
    """
    Encrypt a password

    Parameters:
      key (bytestring) key to use for encryption and later decryption
      password (string) password to be encrypted

    """
    f = Fernet(key)
    token = f.encrypt(password.encode())
    return token


def decrypt_password(key, encrypted_password):
    """
    Decrypt a password

    Parameters:
      key (bytestring) key to use for decryption
      password (string) password to be decrypted

    """
    f = Fernet(key)
    password = f.decrypt(encrypted_password.encode())
    return password.decode()
