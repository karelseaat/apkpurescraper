#!/usr/bin/env python

# https://pypi.org/project/requests-tor/
# https://androidapksfree.com/

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


def process_results(multy):

    result, page = multy

    playstoreapp = session.query(Playstoreapp).filter(Playstoreapp.appid == result['appId']).first()
    if not playstoreapp:
        playstoreapp = Playstoreapp()

    playstoreapp.appid = result['appId']
    playstoreapp.downloads = result['minInstalls']
    playstoreapp.rating = result['score']
    playstoreapp.reviews = result['reviews']
    playstoreapp.developer = result['developer']
    if result['developerWebsite']:
        playstoreapp.devwebsite = result['developerWebsite'][:127]
    if result['developerAddress']:
        playstoreapp.address = result['developerAddress'][:127]
    playstoreapp.adds = result['adSupported']
    playstoreapp.title = result['title']
    playstoreapp.inapp = result['offersIAP']
    playstoreapp.icon = result['icon']


    genre = session.query(Genre).filter(Genre.name == result['genre']).first()
    if not genre:
        genre = Genre()
        genre.name = result['genre']
    playstoreapp.genres.append(genre)

    if result['released']:
        playstoreapp.releasedon = datetime.strptime(result['released'], '%b %d, %Y')

    if result['updated']:
        playstoreapp.lastupdate = datetime.fromtimestamp(int(result['updated']))
    playstoreapp.about = result['description'][:255]
    playstoreapp.price = result['price']

    page.playstoreapp = playstoreapp



    session.add(page)

def crawlapage(page):
    page.lastplaycrawl = datetime.now()
    session.add(page)
    try:
        result = app(page.appid)
        print("app found: ", page.appid)
        return result

    except Exception as e:
        print(e, page.appid)
        return None



def make_session():
    engine = create_engine("mysql+pymysql://root:password@localhost/test?charset=utf8mb4", echo=False)
    dbsession = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return dbsession()

session = make_session()

results = []

while True:

    print("getting app ids")
    crawls = (session
            .query(Appurl)
            .filter(Appurl.done == True)
            .order_by(Appurl.lastplaycrawl)
            .limit(50)
            .all()
        )

    print("clawling app ids")
    for crawl in crawls:
        result = crawlapage(crawl)
        if result:
            results.append((result, crawl))
        time.sleep(2)


    print("crawl done, processing results")
    for result in results:
        process_results(result)

    results = []
    print("commiting!")
    session.commit()
