from .globals import Colors

##
def error_message(function_name:str, e:object)->None:
    print(f"{function_name} {Colors.ANSI_COLOR_RED}ERROR{Colors.ANSI_COLOR_NO} {e}")
