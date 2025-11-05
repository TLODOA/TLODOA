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
    path_splited = path.split('/')
    equal = False

    for i in app.url_map.iter_rules():
        i = str(i)
        i_splited = i.split('/')
        # print('rule_splited: ', i_splited)
        # print('path_splited: ', path_splited)

        if len(path_splited) != len(i_splited):
            continue

        for j in range(len(path_splited)):
            if re.search("^<.*>$", i_splited[j]):
                continue

            if path_splited[j] != i_splited[j]:
                equal = False
                break

            equal = True

        if equal:
            break

    return equal
