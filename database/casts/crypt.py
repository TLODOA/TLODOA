from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from begin.globals.Token import MASTER_KEY

import base64
import os

##
def key_wrap(dek:bytes, master_key:bytes=MASTER_KEY)->str:
    aesgcm = AESGCM(master_key)

    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, dek, None)
    return base64.b64encode(nonce + ciphertext).decode()

def key_unwrap(dek:str, master_key:bytes=MASTER_KEY)->bytes:
    aesgcm = AESGCM(master_key)
    data = base64.b64decode(dek)

    nonce = data[:12]
    ciphertext = data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None)


def field_encrypt(dek:bytes, value:str)->str|None:
    if value is None:
        return None

    aesgcm = AESGCM(dek)

    nonce = os.urandom(12)
    plaintext = value.encode()
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    return base64.b64encode(nonce + ciphertext).decode()

def field_decrypt(dek:bytes, value:str)->str:
    aesgcm = AESGCM(dek)
    data = base64.b64decode(value)

    nonce = data[:12]
    ciphertext = data[12:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    return plaintext.decode()
