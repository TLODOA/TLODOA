from .casts import Base

from begin import error_message

import sqlalchemy

##
def foreign_key_enable(conn, branch)->None:
    conn.execute('PRAGMA foreign_keys = ON')


engine = sqlalchemy.create_engine("sqlite:///data.db", echo=True)

sqlalchemy.event.listen(engine, 'connect', foreign_key_enable)

Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

##
def session_insert(model:object, **kwargs)->object:
    try:
        instance = model(**kwargs)
        session.add(instance)

        session.commit()
    except Exception as e:
        session.rollback()
        error_message('session_insert', e)

    return instance

def session_delete(instance:object)->None:
    try:
        session.delete(instance)
        session.commit()
    except Exception as e:
        session.rollback()
        error_message('session_delete', e)

def session_update(instance:object, attr_name:str, attr_value_new:int)->None:
    try:
        instance.__dict__[attr_name] = attr_value_new
        session.commit()
    except Exception as e:
        session.rollback()
        error_message('session_update', e)
