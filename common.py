from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
from config import connection_string


def make_session():
    engine = create_engine(connection_string, echo=False,  pool_pre_ping=True)
    dbsession = scoped_session(sessionmaker(bind=engine, autoflush=False))
    Base.metadata.create_all(engine)
    return dbsession()
