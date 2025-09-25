from .colors import *

##
def error_message(function_name:str, e:object)->None:
    print(f"{function_name} {ANSI_COLOR_RED}ERROR{ANSI_COLOR_NO} {e}")
