from .session import session
from .methods.crypt import *

from begin.globals import Messages

import re

##
FIELD_CIPHER = lambda model : [ i for i in model.__dict__.keys() if re.search("^cipher_*.", i) ]
FIELD_HASHED = lambda model : [ i for i in model.__dict__.keys() if re.search("^hashed_*.", i) ]

op_comp = {
    'lt': lambda column, value: column < value,
    'lte': lambda column, value: column <= value,

    'gt': lambda column, value: column < value,
    'gte': lambda column, value: column <= value,

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
        Messages.error('session_insert', e)
        session.rollback()

def session_delete(instances:tuple)->None:
    try:
        for i in instances:
            session.delete(i)

        session.commit()
    except Exception as e:
        session.rollback()
        Messages.error('session_delete', e)

def session_update(instances:tuple, **kwargs)->None:
    from begin.globals import Token

    ##
    try:
        for i in instances:
            model_update(i, **kwargs)

        session.commit()

    except Exception as e:
        session.rollback()
        Messages.error('session_update', e)

def session_query(model:object, **kwargs)->tuple|None:
    from begin.globals import Token

    ##
    try:
        instances_get = ()
        filters = []

        for i in kwargs.keys():
            op = None
            column_name = op_type = None

            if '__' in i:
                column_name, op_type = i.split('__')
            else: 
                column_name, op_type = i, 'eq'

            op = op_comp[op_type]
            filters.append(op(model.__dict__[column_name], kwargs[i]))

        instances_get = session.query(model).filter(*filters).all()
        return instances_get

    except Exception as e:
        Messages.error(e, 'session_get')

        return None

##
def model_args_filter(model:object, **kwargs)->dict:
    from begin.globals import Token

    ##
    field_cipher = FIELD_CIPHER(model)
    field_hashed = FIELD_HASHED(model)

    kwargs_copy = kwargs.copy()

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

        model_args = model_args_filter(model, **kwargs_copy)
        instance = model(**model_args)

        return instance

    except Exception as e:
        Messages.error('model_create', e)
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
        Messages.error('model_update', e)
        session.rollback()

def model_get(instance:object, *args)->list|None:
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

        return values

    except Exception as e:
        Messages.error("model_get", e)

        return None
