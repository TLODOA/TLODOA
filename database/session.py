from begin import error_message
from begin.xtensions import *

from .casts import Base
from .crypt import *

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


##
def foreign_key_enable(conn, branch)->None:
    conn.execute('PRAGMA foreign_keys = ON')


engine = sqlalchemy.create_engine("sqlite:///data.db", echo=True)

sqlalchemy.event.listen(engine, 'connect', foreign_key_enable)

Base.metadata.create_all(engine)

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
        dek = AESGCM.generate_key(bit_length=256)
        kwargs["dek"] = key_wrap(dek, MASTER_KEY)

        model_sample = model()
        field_encrypted = getattr(model_sample, "FIELD_ENCRYPTED", [])
        field_hashed = getattr(model_smaple, "FIELD_HASHED", [])

        for i in kwargs.keys():
            if not i in field_encrypt and not i in field_hashed:
                continue

            if i in field_hashed:
                kwargs[i] = Token.crypt_sha256(SALT_GLOBAL, kwargs[i])
                continue

            kwargs[i] = field_encrypt(dek, kwargs[i])

        #
        instance = model(**kwargs)

        session.add(instance)
        session.commit()

        return instance

    except Exception as e:
        session.rollback()
        error_message('session_insert', e)


def session_delete(instance:tuple)->None:
    try:
        for i in instance:
            session.delete(i)

        session.commit()
    except Exception as e:
        session.rollback()
        error_message('session_delete', e)

def session_update(instance:tuple, attr_name:str, attr_value_new:int)->None:
    from begin.globals import Token

    try:
        field_encrypted = getattr(instance[0], "FIELD_ENCRYPTED", [])
        field_hashed = getattr(instance[0], "FIELD_HASHED", [])

        for i in instance:
            dek = key_unwrap(i.dek, MASTER_KEY)

            #
            if not i in field_encrypted and not i in field_hashed:
                setattr(i, attr_name, attr_value_new)
                continue

            if i in field_hashed:
                setattr(i, attr_name, Token.crypt_hash256(attr_value_new))
                continue

            setattr(i, attr_name, field_encrypt(dek, attr_value_new))

        session.commit()
    except Exception as e:
        session.rollback()
        error_message('session_update', e)

def session_get(model:object, **kwargs)->tuple|None:
    from begin.globals import Token

    try:
        model_sample = model()
        field_hashed = getattr(model_sample, "FIELD_HASHED", [])

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

            if not i in field_hashed:
                filters.append(op(model.__dict__[column_name], kwargs[i]))
                continue

            filters.append(op(model.__dict__[column_name], Token.crypt_hash256(kwargs[i])))

        instances_get = session.query(model).filter(*filters).all()

        return instances_get

    except Exception as e:
        error_message(e, 'session_get')

        return None
