def cookie_define(response:object, cookie_name:str, cookie_value, max_age:int=60*60*24)->None:
    response.set_cookie(cookie_name, cookie_value, secure=True, httponly=True, max_age=max_age)
