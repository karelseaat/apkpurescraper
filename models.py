

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, String, Integer, Boolean, Date, DateTime
from sqlalchemy_utils import get_hybrid_properties
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base(name="Base")
metadata = Base.metadata

class Appurl(Base):
    __tablename__ = 'rankingapp'
    id = Column(Integer, primary_key=True)
    appid = Column(String(128), nullable=False, unique=True)
    appurl = Column(String(128), nullable=False)
    done = Column(Boolean, default=False)
    inplaystore = Column(Boolean, default=False)
    playstoreapp_id = Column(ForeignKey('playstoreapp.id'), index=True)
    playstoreapp = relationship('Playstoreapp', back_populates="rawapp")


app_genre_association = Table('appgenre', Base.metadata,
    Column('playstoreapp_id', ForeignKey('playstoreapp.id')),
    Column('genre_id', ForeignKey('genre.id'))
)

class Playstoreapp(Base):
    __tablename__ = 'playstoreapp'
    id = Column(Integer, primary_key=True)
    appid = Column(String(128), nullable=False)
    downloads = Column(Integer)
    reviews = Column(Integer)
    rating = Column(Integer)
    developer = Column(String(128), nullable=False)
    inapp = Column(Boolean, default=False)
    adds = Column(Boolean, default=False)
    title = Column(String(128))
    lastupdate = Column(DateTime)
    about = Column(String(256))
    price = Column(Integer)
    lastcrawled = Column(DateTime, default=datetime.datetime.utcnow)
    releasedon = Column(DateTime)
    icon = Column(String(128))
    devwebsite = Column(String(128))
    address = Column(String(128))
    size = Column(Integer)


    genres = relationship(
        "Genre",
        secondary=app_genre_association,
        back_populates="apps",
    )

    rawapp = relationship('Appurl', back_populates="playstoreapp")

class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)

    apps = relationship(
        "Playstoreapp",
        secondary=app_genre_association,
        back_populates="genres",
    )
