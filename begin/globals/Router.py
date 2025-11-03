import importlib
import inspect

import re
import os

##
DIR_PATH = "routers"

REGISTER_IGNORE = []

#
"""
Due to groups as skilled as us,
we use the ArturRegadas autction project code as base for this file
"""

def register(app:object, folder:str=DIR_PATH)->None:
    folder_path = os.path.abspath(folder)
    
    for file in os.listdir(folder_path):
        file_path = f"{folder_path}/{file}"

        if not os.path.isfile(file_path):
            register(app, file_path)
            continue

        if not re.search("^routers_.*\.py$", file) or file in REGISTER_IGNORE:
            continue

        ##
        module_name = file[:-3]
        module_spec = importlib.util.spec_from_file_location(module_name, file_path)

        if not module_spec or not module_spec.loader :
            continue

        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        # print(module_name)
        module.register_app(app)

def exists(app:object, path:str)->bool:
    for i in app.url_map.iter_rules():
        if i.rule == path or i.rule.split('<')[0] == path.split('<')[0]:
            return True

    return False
