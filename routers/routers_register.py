"""
Due to groups as skilled as us,
we use the ArturRegadas autction project code as base for this file
"""

from begin import *

import importlib
import inspect

##
def router_register(app:object, folder:str)->None:
    folder_path = os.path.abspath(folder)
    
    for file in os.listdir(folder_path):
        if file in ROUTER_REGISTER_IGNORE:
            continue

        file_extension = file.split('.')[-1]
        file_path = f"{folder_path}/{file}"

        if file_extension != 'py' and not os.path.isfile(file_path):
            router_register(app, file_path)
            continue
        elif file_extension != 'py':
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
