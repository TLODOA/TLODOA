from .session import session
from .methods.crypt import *

from begin.globals import Messages

import re

##
FIELD_CIPHER = lambda model : [ i for i in model.__dict__.keys() if re.search("^cipher_.*", i) ]
FIELD_HASHED = lambda model : [ i for i in model.__dict__.keys() if re.search("^hashed_.*", i) ]
FIELD_DEFAULT = lambda model : [ i for i in model.__dict__.keys() if re.search("^DEFAULT_.*", i) ]

op_comp = {
    'lt': lambda column, value: column < value,
    'lte': lambda column, value: column <= value,

    'gt': lambda column, value: column > value,
    'gte': lambda column, value: column >= value,

    'eq': lambda column, value: column == value,
    'ne': lambda column, value: column != value,
    'in': lambda column, value: column.in_(value)
}

##
def session_insert(model:object, **kwargs)->object:
    try:
        instance = model_create(model, **kwargs)

        session.add(instance)
        session.commit()

        return instance

    except Exception as e:
        Messages.Error.print('session_insert', e)
        session.rollback()

def session_delete(instances:tuple)->None:
    try:
        for i in instances:
            session.delete(i)

        session.commit()
    except Exception as e:
        session.rollback()
        Messages.Error.print('session_delete', e)

def session_update(instances:tuple, **kwargs)->None:
    from begin.globals import Token

    ##
    try:
        for i in instances:
            model_update(i, **kwargs)

        session.commit()

    except Exception as e:
        session.rollback()
        Messages.Error.print('session_update', e)

def session_query(model:object, **kwargs)->tuple|None:
    from begin.globals import Token

    ##
    try:
        field_cipher = FIELD_CIPHER(model)
        instances_get = ()
        filters = []

        #
        filter_args = model_args_filter(model, **kwargs)

        for i in kwargs.keys():
            if i in filter_args.keys():
                continue

            column_name, op = i, 'eq'
            if '__' in i:
                column_name, op = i.split('__')

            if not column_name in model.__dict__.keys() or not op in op_comp.keys():
                continue

            filter_args[i] = kwargs[i]

        print('kwargs: ', kwargs)
        print('filter_args: ', filter_args)
        ##
        for i in filter_args.keys():
            op = None
            column_name = op_type = None

            column_name, op_type = i, 'eq'
            if '__' in i:
                column_name, op_type = i.split('__')

            if not op_type in op_comp.keys():
                continue

            #
            op = op_comp[op_type]
            column = getattr(model, column_name, None)
            print(column, filter_args[i])

            filters.append(op(column, filter_args[i]))

        instances_get = session.query(model).filter(*filters).all()
        return instances_get

    except Exception as e:
        Messages.Error.print(e, 'session_query')

        return None

##
def model_args_filter(model:object, **kwargs)->dict:
    from begin.globals import Token

    ##
    field_cipher = FIELD_CIPHER(model)
    field_hashed = FIELD_HASHED(model)

    kwargs_copy = kwargs.copy()

    ##
    for i in field_cipher:
        dek_wrap = kwargs_copy.get("dek", None)
        if dek_wrap is None:
            break

        dek = dek_decrypt(dek_wrap)
        _, attr_name = i.split('cipher_')

        if not attr_name in kwargs_copy.keys() or i in kwargs_copy.keys():
            continue

        kwargs_copy[i] = clm_encrypt(kwargs_copy[attr_name], dek)

    for i in field_hashed:
        _, attr_name = i.split('hashed_')

        if not attr_name in kwargs_copy.keys() or i in kwargs_copy.keys():
            continue

        kwargs_copy[i] = Token.crypt_sha256(kwargs_copy[attr_name])


    ##
    for i in list(kwargs_copy.keys()):
        if i in model.__dict__.keys():
            continue

        del kwargs_copy[i]

    return kwargs_copy

def model_create(model:object, **kwargs)->object|None:
    try:
        kwargs_copy = kwargs.copy()
        if not "dek" in kwargs_copy.keys() and "dek" in model.__dict__.keys():
            kwargs_copy["dek"] = dek_encrypt(dek_generate())

        ##
        field_cipher = FIELD_CIPHER(model)
        field_hashed = FIELD_HASHED(model)
        default_value = FIELD_DEFAULT(model)

        for i in default_value:
            _, attr_name = i.split('DEFAULT_')
            if attr_name in kwargs.keys():
                continue

            for j in field_cipher:
                if not re.search(f".*_{attr_name}$", j):
                    continue

                kwargs_copy[attr_name] = model.__dict__[i]
                break

            for j in field_hashed:
                if not re.search(f".*_{attr_name}$", j):
                    continue

                kwargs_copy[attr_name] = model.__dict__[i]
                break
            
            if attr_name in model.__dict__.keys():
                kwargs_copy[attr_name] = model.__dict__[i]

        ##
        print('kwargs_copy', kwargs_copy)
        model_args = model_args_filter(model, **kwargs_copy)
        print('model_args: ', model_args, field_cipher)
        instance = model(**model_args)

        return instance

    except Exception as e:
        Messages.Error.print('model_create', e)
        session.rollback()

        return None

def model_update(instance:object, **kwargs)->None:
    from begin.globals import Token

    ##
    try:
        model = type("Model", (instance.__class__, ), {})
        model_args = model_args_filter(model, **kwargs, dek=getattr(instance, "dek", None))

        for i in model_args.keys():
            setattr(instance, i, model_args[i])

        session.commit()

    except Exception as e:
        Messages.Error.print('model_update', e)
        session.rollback()

def model_get(instance:object, *args)->tuple|None:
    try:
        model = type("Model", (instance.__class__, ), {})

        field_cipher = FIELD_CIPHER(model)
        field_hashed = FIELD_HASHED(model)
        
        #
        values = []

        for i in args:
            dek_wrap = getattr(instance, "dek", None)
            dek = dek_decrypt(dek_wrap) if not dek_wrap is None else None

            value = getattr(instance, i, None)
            if value is None:
                continue

            if not dek is None and i in field_cipher:
                values.append(clm_decrypt(value, dek))
                continue

            values.append(value)

        if not len(values):
            values = [ None ]

        return tuple(values)

    except Exception as e:
        Messages.Error.print("model_get", e)

        return None


def model_unwrap(instance:object)->dict|None:
    try:
        model = type("model", (instance.__class__, ), {})

        field_cipher = FIELD_CIPHER(model)
        field_hashed = FIELD_HASHED(model)

        instance_unwrap = {}

        #
        for i in instance.__dict__.keys():
            if i == '_sa_instance_state' or i == 'dek':
                continue

            key_name = i if not i in field_cipher else i.split('cipher_')[1]
            instance_unwrap[key_name] = model_get(instance, i)[0]

        return instance_unwrap

    except Exception as e:
        Messages.Error.print('model_unwrap', e)
        session.rollback()

        return None
