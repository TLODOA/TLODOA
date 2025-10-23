
AUTH_ATTEMPTS_MAX = 30

#
KEY_EMAIL_CHARS = '0123456789abcdefghijklmnopqrstuvwxyz'
KEY_EMAIL_LEN = 8

KEY_USER_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
KEY_USER_LEN = 32

#
HASH_EMAIL_TOKEN_LEN = 32

HASH_USER_PASSWORD_LEN = 32
HASH_USER_TOKEN_LEN = 32

#
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
