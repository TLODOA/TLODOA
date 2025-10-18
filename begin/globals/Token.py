
AUTH_ATTEMPTS_MAX = 30

KEY_EMAIL_CHARS = '0123456789abcdefghijklmnopqrstuvwxyz'
KEY_EMAIL_LEN = 7

##
def email_generate()->str:
    import secrets

    return ''.join(secrets.choice(KEY_EMAIL_CHARS) for _ in range(KEY_EMAIL_LEN))
