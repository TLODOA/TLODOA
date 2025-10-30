import importlib
import inspect
import re
import os


##
def init()->object:
    from apscheduler.schedulers.background import BackgroundScheduler

    ##
    return BackgroundScheduler()

##
REGISTER_IGNORE = []
DIR_PATH = 'schedulers'

def register(scheduler:object, file_name:str=DIR_PATH)->None:
    folder_path = os.path.abspath(file_name)

    for file_name in os.listdir(folder_path):
        file_path = f"{folder_path}/{file_name}"

        if not os.path.isfile(file_path):
            register(scheduler, file_path)
            continue

        if not re.search("^jobs_.*\.py$", file_name) or file_name in REGISTER_IGNORE:
            continue

        ##
        module_name = file_name[-3]
        module_spec = importlib.util.spec_from_file_location(module_name, file_path)

        if not module_name or not module_spec.loader:
            continue

        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        #
        jobs = module.jobs()

        for i in jobs:
            print(i.func, i.seconds)
            scheduler.add_job(func=i.func, trigger=i.trigger, seconds=i.seconds)

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
