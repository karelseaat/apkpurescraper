from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

def make_session():
    engine = create_engine("mysql+pymysql://root:kateobele@192.168.2.123/apkscraper?charset=utf8mb4", echo=False)
    dbsession = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return dbsession()

def make_proxy_session():
    engine = create_engine("mysql+pymysql://root:kateobele@localhost/proxymaster?charset=utf8mb4", echo=False)
    dbsession = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return dbsession()
