
REGISTER_IGNORE = []

DIR_PATH = 'schedulers'

##
TRIGGER = "interval"
SECONDS = 60*60*24

class Task():
    def __init__(self, func:object=None \
            ,trigger:str=TRIGGER \
            ,seconds:int=SECONDS):

        self.func = func
        self.trigger = trigger
        self.seconds = seconds
