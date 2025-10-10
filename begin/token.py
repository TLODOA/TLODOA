from .globals import TOKEN_EMAIL_CHARS, TOKEN_EMAIL_LEN

import secrets
import string

def token_email_generate()->str:
    return ''.join(secrets.choice(TOKEN_EMAIL_CHARS) for _ in range(TOKEN_EMAIL_LEN))
