

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, String, Integer, Boolean, Date
from sqlalchemy_utils import get_hybrid_properties
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base(name="Base")
metadata = Base.metadata

class Appurl(Base):
    """an sqlalchemy model for the rank of an app"""
    __tablename__ = 'rankingapp'
    id = Column(Integer, primary_key=True)
    url = Column(String(128), nullable=False)
    done = Column(Boolean, default=False)
