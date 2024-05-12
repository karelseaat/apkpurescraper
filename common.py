from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

one_or_zero = 0

def make_session():
    engine = create_engine("mysql+pymysql://root:kateobele@192.168.2.124/apkscraper?charset=utf8mb4", echo=False,  pool_pre_ping=True)
    dbsession = scoped_session(sessionmaker(bind=engine, autoflush=False))
    Base.metadata.create_all(engine)
    return dbsession()
