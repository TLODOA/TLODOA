import os

##
AUTH_ATTEMPTS_MAX = 30

#
DEK_LEN = 80

##
KEY_EMAIL_CHARS = '0123456789abcdefghijklmnopqrstuvwxyz'
KEY_EMAIL_LEN = 8

KEY_USER_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
KEY_USER_LEN = 32

##
HASH_EMAIL_TOKEN_LEN = 32

HASH_USER_PASSWORD_LEN = 32
HASH_USER_TOKEN_LEN = 32

##
VALIDITY_KEY_USER = 60*60*24 # one day

VALIDITY_IPINFOS = 60*60*24*7 # one week
VALIDITY_IPINFOS_BLOCK = 60*20 # twenty minutes

##
def email_generate()->str:
    import secrets

    return ''.join(secrets.choice(KEY_EMAIL_CHARS) for _ in range(KEY_EMAIL_LEN))

def user_generate()->str:
    import secrets

    return ''.join(secrets.choice(KEY_USER_CHARS) for _ in range(KEY_USER_LEN))


def crypt_hash(text, **kwargs)->str:
    from argon2 import PasswordHasher

    ##
    hasher = PasswordHasher(**kwargs)

    return hasher.hash(text)

def crypt_hash_auth(text_hasher, text)->bool:
    from argon2 import PasswordHasher

    ##
    hasher = PasswordHasher()

    try:
        return hasher.verify(text_hasher, text)

    except:
        return False


def crypt_hash256(salt:bytes, text:str)->str:
    import hashlib
    import base64

    ##
    value_hasehd = hashlib.sha256(salt + text.encode()).digest()
    return base64.b64encode(value_hashed).decode()


def crypt_aes(text=None, key_length=32, key=None)->str:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding

    import os
    import base64

    ##
    if key is None:
        key = os.urandom(key_length)

    text = text.encode()

    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()
    text_padded = padder.update(text) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    text_encrypted = encryptor.update(text_padded) + encryptor.finalize()
    text_encrypted_64 = base64.b64encode(iv + text_encrypted).decode()

    return text_encrypted_64

def decrypt_aes(text=None, key=None)->str:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding

    import base64

    ##
    data = base64.b64decode(text.encode())
    iv = data[:16]
    text_encrypted = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    text_encrypted_padded = decryptor.update(text_encrypted) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    text = unpadder.update(text_encrypted_padded) + unpadder.finalize()

    return text
