from begin import error_message
from begin.xtensions import *

from .casts import Base
from .casts.crypt import *

##
def foreign_key_enable(conn, branch)->None:
    conn.execute('PRAGMA foreign_keys = ON')

def reset_database(engine:object):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

engine = sqlalchemy.create_engine("sqlite:///data.db", echo=True)
sqlalchemy.event.listen(engine, 'connect', foreign_key_enable)

# Base.metadata.create_all(engine)
reset_database(engine)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

##
operator_comp = {
    'lt': lambda column, value: column < value,
    'lte': lambda column, value: column <= value,

    'gt': lambda column, value: column < value,
    'gte': lambda column, value: column <= value,

    'eq': lambda column, value: column == value,
    'ne': lambda column, value: column != value,
    'in': lambda column, value: column.in_(value)
}

#
def session_insert(model:object, **kwargs)->object:
    from begin.globals import Token

    try:
        instance = model(**kwargs)

        session.add(instance)
        session.commit()

        return instance

    except Exception as e:
        error_message('session_insert', e)
        session.rollback()

def session_delete(instance:tuple)->None:
    try:
        for i in instance:
            session.delete(i)

        session.commit()
    except Exception as e:
        session.rollback()
        error_message('session_delete', e)

def session_update(instance:tuple, **kwargs)->None:
    from begin.globals import Token

    try:
        for i in instance:
            model_update(i, **kwargs)

        session.commit()

    except InvalidTag:
        error_message('session_update', 'Invalid MASTER_KEY')

    except Exception as e:
        error_message('session_update', e)

    finally:
        session.rollback()

def session_get(model:object, **kwargs)->tuple|None:
    from begin.globals import Token

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

            op = operator_comp[op_type]
            filters.append(op(model.__dict__[column_name], kwargs[i]))

        instances_get = session.query(model).filter(*filters).all()
        return instances_get

    except Exception as e:
        error_message(e, 'session_get')

        return None


def model_get(instance:object, *args)->list|None:
    try:
        model = type("Model", (instance.__class__, ), {})

        field_encrypted = getattr(model, "FIELD_CIPHER", [])
        field_hashed = getattr(model, "FIELD_HASHED", [])
        
        #
        values = []
        for i in args:
            print(instance.dek)
            attr = getattr(instance, i, None)

            #
            dek = key_unwrap(instance.dek)
        
            if i in field_encrypted:
                attr = field_decrypt(dek, attr)

            values.append(attr)

        return values

    except Exception as e:
        error_message("model_get", e)

        return None

def model_update(instance:object, **kwargs)->None:
    from begin.globals import Token

    ##
    try:
        model = type("Model", (instance.__class__, ), {})

        field_cipher = getattr(model, "FIELD_CIPHER", [])
        field_hashed = getattr(model, "FIELD_HASHED", [])

        for i in kwargs.keys():
            dek = key_unwrap(instance.dek)
            value = kwargs[i]

            if i in field_hashed:
                value = Token,crypt_hash256(kwars[i])
            elif i in field_cipher:
                value = field_encrypt(dek, value)

            setattr(instance, i, value)

        session.commit()

    except Exception as e:
        error_message('model_update', e)
        session.rollback()
