ANSI_COLOR_RED = '\033[91m'
ANSI_COLOR_NULL = '\033[0m'

##
class Message():
    def __init__(self, type:str, content:str):
        self.type = type
        self.content = content

    @property
    def json(self)->dict:
        return {
            "content": self.content,
            "type": self.type
        }

##
class Error():
    js_class="log_message_erro"

    def print(func_name:str, e:object)->None:
        print(f"{func_name} {ANSI_COLOR_RED}ERROR{ANSI_COLOR_NULL}: {e}")

class Success():
    js_class = "log_message_ok"

## Request
class Request():
    class Error(Error):
        internal = "Something goes wrong"

        invalid_method = "Method not allow"
        invalid_fields = "Invalid fields"

        missing_fields = "Missing fields"
        empty_fields = "Please, fill all required fields"

        def invalid_client_behavior(timestamp):
            import time

            date = time.localtime(timestamp)

            return f"Because of your behavior, you cannot try sign after {date.tm_hour}:{date.tm_min}:{date.tm_sec}"

## Email
class Email():
    class Request(Request):
        pass

    class Error(Error):
        def invalid_interval(timestamp)->str:
            import time

            date = time.localtime(timestamp)

            return f"You request an email recently, asked other at {date.tm_hour}:{date.tm_min}:{date.tm_sec}s"

        def invalid_amount(timestamp)->str:
            import time

            date = time.localtime(timestamp)

            return f"You request many emails once. Plase, wait until {date.tm_hour}:{date.tm_min}:{date.tm_sec}s to do other request"

        def invalid_token_attempts(timestamp)->str:
            import time

            date = time.localtime(timestamp)

            return f"You do many attempts of token authentication once, try again in {date.tm_hour}:{date.tm_min}:{date.tm_sec}"

        def ip_blocked(timestamp)->str:
            import time

            date = time.localtime(timestamp)

            return f"You ip was be blocked because of your activity, try send email again after {date.tm_hour}:{date.tm_min}:{date.tm_sec}"

        already_sended = "You alread receive the email"

    class Success(Success):
        ok = "Emaill successful send!"

class EmailCode():
    class Request(Request):
        pass

    class Email(Email):
        pass

    class Error(Error):
        incorrect_code = "Email Code incorrect"
        code_not_send = "Email code not requested"

        invalid_code_validity = "Email token was be expired"
        
## Login auth
class Login():
    class Error(Error):
        user_not_found = "User not found"
        already_ip_logged = "This ip is already logged"

        incorrect_user_email = "User email incorrect"
        incorrect_user_password = "User password incorrect"

    class EmailCode(EmailCode):
        pass

    class Request(Request):
        pass

## Sing auth
class Sign(Login):
    class Error(Login.Error):
        user_found = "Invalid user name"
        password_not_match = "Passwords not match"

## Profile edit
class ProfileEdit():
    class Error(Error):
        user_not_found = "This user doens't exist"
        icon_not_found = "The selected icon doen't exist"

    class Request(Request):
        pass

    class Success(Success):
        ok = "User successful modified!"

## Object creation
class ObjectCreation():
    class Error(Error):
        invalid_file_size = "Plase, insert a file small"

    class Request(Request):
        pass

    class Success(Success):
        ok = "Object succefully created!"
