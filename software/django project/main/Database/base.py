# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


def init():
    global session
    global Base
    global engine
    databasename = "test.sqlite"
    engine = create_engine('sqlite:///'+databasename)
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)
    Base = declarative_base()
    print(session!=None)
    
def makeMetaData():
    Base.metadata.create_all(engine)



