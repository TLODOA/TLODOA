
def request_not_allow_because_method()->str:
    return "Method not allow"

def server_internal_error()->str:
    return "Something goes wrong"

## Email
def email_not_allow_because_interval(timestamp)->str:
    import time

    date = time.localtime(timestamp)

    return f"You request an email recently, asked other at {date.tm_hour}:{date.tm_min}:{date.tm_sec}s"

def email_not_allow_because_amount(timestamp)->str:
    import time

    date = time.localtime(timestamp)

    return f"You request many emails once. Plase, wait until {date.tm_hour}:{date.tm_min}:{date.tm_sec}s to do other request"

def email_already_sended()->str:
    return "You already receive the email"

def email_ok()->str:
    return "Email successful sended!"

## Sign auth
def sign_not_allow_because_user_not_found()->str:
    return "User not found"

def sign_not_allow_because_user_email_incorrect()->str:
    return "User email incorrect"

def sign_not_allow_because_user_password_incorrect()->str:
    return "User password incorrect"


def sign_not_allow_because_email_code_incorrect()->str:
    return "Email code incorrect"
