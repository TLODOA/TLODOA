
AUTH_ATTEMPTS_MAX = 30

KEY_EMAIL_CHARS = '0123456789abcdefghijklmnopqrstuvwxyz'
KEY_EMAIL_LEN = 7

KEY_USER_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
KEY_USER_LEN = 20

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
