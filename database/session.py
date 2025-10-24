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
    try:
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
    try:
        for i in instance:
            setattr(i, attr_name, attr_value_new)

        session.commit()
    except Exception as e:
        session.rollback()
        error_message('session_update', e)

def session_get(model:object, **kwargs)->tuple|None:
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
