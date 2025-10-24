from cryptography.hazmat.primitives.ciphers.aead import AESGCM

"""
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.hazmat.primitives import hashes
"""

import os

##
MASTER_KEY = os.environ.get("MASTER_KEY", None)
SALT_GLOBAL = os.environ.get("SALT_GLOBAL", None)

if MASTER_KEY is None:
    MASTER_KEY = AESGCM.generate_key(bit_length = 256)

if SALT_GLOBAL is None:
    SALT_GLOBAL = os.urandom(32)

#
def key_wrap(dek:bytes, master_key:bytes)->str:
    import base64

    ##
    aesgcm = AESGCM(master_key)

    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, dek, None)

    return base64.b64encode(nonce + ciphertext).decode()

def key_unwrap(dek:bytes, master_key:bytes)->bytes:
    import base64

    ##
    data = base64.b64decode(dek)

    nonce = data[:12]
    ciphertext = data[12:]

    aesgcm = AESGCM(master_key)

    return aesgcm.decrypt(nonce, ciphertext, None)


def field_encrypt(dek:bytes, value:object)->str:
    import base64

    ##
    aesgcm = AESGCM(dek)

    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, dek, None)

    return base64.b64encode(nonce + ciphertext).decode()

def field_decrypt(dek:bytes, value:object)->str:
    import base64

    ##
    data = base64.b64decode(value)

    nonce = value[:12]
    ciphertext = value[12:]

    aesgcm = AESGCM(dek)

    return aesgcm.decrypt(nonce, ciphertext, None)

"""
##
try:
    dek = AESGCM.generate_key(bit_length=256)
    key_alternate = AESGCM.generate_key(bit_length=256)

    dek_wrapped = key_wrap(dek, MASTER_KEY)
    dek_unwrapped = key_unwrap(dek_wrapped, MASTER_KEY)

    print(dek_unwrapped)

except Exception as e:
    print(e)
"""
