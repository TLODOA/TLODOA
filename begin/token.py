from .globals import Token

import secrets
import string

##
def token_email_generate()->str:
    return ''.join(secrets.choice(Token.KEY_EMAIL_CHARS) for _ in range(Token.KEY_EMAIL_LEN))
