from sqlalchemy import MetaData, text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

##
def sqlite_database_create(engine:object)->object:
    with open('./database/casts/schema_sqlite.sql', 'r') as file:
        sql = file.read()

    with engine.connect() as connection:
        for i in sql.split(';'):
            connection.execute(text(i))

        connection.commit()

    metadata = MetaData()
    metadata.reflect(bind=engine)

    Base = declarative_base(metadata=metadata)
    return Base

def sqlite_database_drop_tables(engine:object)->None:
    metadata = MetaData()
    metadata.reflect(bind=engine)

    metadata.drop_all(engine)

def sqlite_database_init()->None:
    global engine

    global Base
    global session

    #
    engine = create_engine("sqlite:///tlodoadb.db", echo=True)

    sqlite_database_drop_tables(engine)
    Base = sqlite_database_create(engine)

    Session = sessionmaker(bind=engine)
    session = Session()


def postgres_database_create(engine:object)->object:
    with open('./database/casts/schema_postgres.sql', 'r') as file:
        sql = file.read()

    with engine.connect() as connection:
        connection.execute(text(sql))
        connection.commit()

    metadata = MetaData()
    metadata.reflect(bind=engine)

    Base = declarative_base(metadata=metadata)
    return Base

def postgres_database_drop_tables(engine:object)->None:
    metadata = MetaData()
    metadata.reflect(bind=engine)

    metadata.drop_all(engine)

def postgres_database_init()->None:
    global engine

    global Base
    global session

    #
    engine = create_engine("postgresql://lorax:admin@localhost/tlodoadb", echo=True)

    postgres_database_drop_tables(engine)
    Base = postgres_database_create(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

#
engine, Base, session = None, None, None

# Not run postgres ? Comment the below line and uncomment the next statement
# postgres_database_init()
sqlite_database_init()
