
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, String, Integer, Boolean, Date, DateTime, BigInteger
from sqlalchemy_utils import get_hybrid_properties
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base(name="Base")
metadata = Base.metadata

class Proxys(Base):
    __tablename__ = 'proxys'
    id = Column(Integer, primary_key=True)
    ip = Column(String(128), nullable=False)
    port = Column(Integer)
    country = Column(String(32))
    proto = Column(String(128))
    anon = Column(Integer)
    delay = Column(Integer)
    google = Column(Boolean)
    lastchecked = Column(DateTime)
    canreachsite = Column(Boolean)
    collected = Column(DateTime,  default=datetime.datetime.utcnow)
    lastup = Column(DateTime)