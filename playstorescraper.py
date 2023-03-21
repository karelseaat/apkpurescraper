#!/usr/bin/env python


# from selenium.webdriver.firefox.options import Options

from models import Appurl, Playstoreapp, Genre

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
import time
from pprint import pprint

from datetime import datetime, timedelta
from google_play_scraper import app

import json

def textmult(text):
    if "K" in text:
        return int(text[:-1]) * 1000
    if "M" in text:
        return int(text[:-1]) * 1000000
    if "B" in text:
        return int(text[:-1]) * 1000000000
    if text:
        return int(text)

    return 0

def crawlapage(page):

    page.inplaystore = False

    try:
        result = app(page.appid)

        playstoreapp = Playstoreapp()
        playstoreapp.appid = page.appid
        playstoreapp.downloads = result['minInstalls']
        playstoreapp.rating = result['score']
        playstoreapp.reviews = result['reviews']
        playstoreapp.developer = result['developer']
        playstoreapp.devwebsite = result['developerWebsite']
        playstoreapp.address = result['developerAddress']
        playstoreapp.adds = result['adSupported']
        playstoreapp.title = result['title']
        playstoreapp.inapp = result['offersIAP']
        playstoreapp.icon = result['icon']

        pprint(result)


        genre = session.query(Genre).filter(Genre.name == result['genre']).first()
        if not genre:
            genre = Genre()
            genre.name = result['genre']
        playstoreapp.genres.append(genre)

        if result['released']:
            playstoreapp.releasedon = datetime.strptime(result['released'], '%b %d, %Y')

        if result['updated']:
            playstoreapp.lastupdate = datetime.fromtimestamp(int(result['updated']))
        playstoreapp.about = result['description']
        playstoreapp.price = result['price']
        session.add(playstoreapp)
        page.inplaystore = True
        page.playstoreapp = playstoreapp

    except Exception as e:
        print(e)

    session.add(page)

    session.commit()
    time.sleep(1)

def make_session():
    engine = create_engine("mysql+pymysql://root:password@localhost/test?charset=utf8mb4", echo=False)
    dbsession = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return dbsession()

session = make_session()
# options = Options()
# options.add_argument("--headless")

allthethings = []


crawls = (session
        .query(Appurl)
        .filter(Appurl.done == True)
        .filter(Appurl.inplaystore == None)
        .all()
    )


for crawl in crawls:
    crawlapage(crawl)

driver.quit()
