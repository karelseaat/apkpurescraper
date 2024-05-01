

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, String, Integer, Boolean, Date, DateTime, BigInteger, JSON
from sqlalchemy_utils import get_hybrid_properties
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base(name="Base")
metadata = Base.metadata


class Newappurl(Base):
    __tablename__ = 'newappurl'
    id = Column(Integer, primary_key=True)
    appid= Column(String(150), nullable=False)
    lastplaycrawl = Column(DateTime)


app_genre_association = Table('appgenre', Base.metadata,
    Column('playstoreapp_id', ForeignKey('playstoreapp.id')),
    Column('genre_id', ForeignKey('genre.id'))
)

class Playstoreapp(Base):
    __tablename__ = 'playstoreapp'
    id = Column(Integer, primary_key=True)
    appid = Column(String(150), nullable=False)
    downloads = Column(BigInteger)
    reviews = Column(Integer)
    rating = Column(Integer, default=0)
    inapp = Column(Boolean, default=False)
    adds = Column(Boolean, default=False)
    title = Column(String(256))
    lastupdate = Column(DateTime)
    allupdates = Column(JSON)
    about = Column(String(512))
    summary = Column(String(256))
    price = Column(Integer)
    releasedon = Column(DateTime)
    icon = Column(String(128))
    devwebsite = Column(String(256), nullable=True)
    removedfromstore = Column(Boolean, default=False)
    hasvideo = Column(Boolean, default=False)
    developer_id = Column(Integer, ForeignKey('developer.id'), nullable=True)
    contentrating_id = Column(Integer, ForeignKey('contentrating.id'))
    privacypolicylink = Column(String(256))
    currentversion = Column(String(32))
    genres = relationship(
        "Genre",
        secondary=app_genre_association,
        back_populates="apps",
    )


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)

    apps = relationship(
        "Playstoreapp",
        secondary=app_genre_association,
        back_populates="genres",
    )

class Developer(Base):
    __tablename__ = 'developer'
    id = Column(Integer, primary_key=True)
    apps = relationship('Playstoreapp', backref='thedeveloper')
    name = Column(String(128), nullable=False)
    address = Column(String(128))
    email = Column(String(256))
    devwebsite = Column(String(256))

class Contentrating(Base):
    __tablename__ = 'contentrating'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    apps = relationship('Playstoreapp', backref='contentrating')
