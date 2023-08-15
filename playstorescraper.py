#!./venv/bin/python3

# https://pypi.org/project/requests-tor/
# https://androidapksfree.com/

from models import Appurl, Playstoreapp, Genre
from proxy_model import Proxys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
import time
from pprint import pprint

from datetime import datetime, timedelta
from google_play_scraper import app
import random
from google_play_scraper.features.app import parse_dom
import requests

# from fastcrc import crc64

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
        print("insert new")
    else:
        print("use existing")

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

    if result['description']:
        playstoreapp.about = result['description'][:255]
    playstoreapp.price = result['price']

    page.playstoreapp = playstoreapp

    session.add(page)


def get_raw(url):



    # proxydict = {"https":f"{proxy.proto}://{proxy.ip}:{proxy.port}"}
    try:
        result = requests.get(url)
        if result.status_code != 200:
            return 0, 1
        else:
            return 1, result
    except Exception as e:
        print(e)
        return 0, 2

def crawlapage(page):
    # global goodproxies

    page.lastplaycrawl = datetime.now()
    # newproxy = random.choice(goodproxies)
    session.add(page)

    url = f"https://play.google.com/store/apps/details?id={page.appid}"
    result = get_raw(url)

    if result[0]:
        return parse_dom(result[1].text, page.appid, url)
    elif result[1] == 2:
        # goodproxies.remove(newproxy)
        return None
    else:
        return None



def make_session():
    engine = create_engine("mysql+pymysql://root:kateobele@localhost/apkscraper?charset=utf8mb4", echo=False)
    dbsession = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return dbsession()


def make_proxy_session():
    engine = create_engine("mysql+pymysql://root:kateobele@localhost/proxymaster?charset=utf8mb4", echo=False)
    dbsession = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return dbsession()

session = make_session()
proxysession = make_proxy_session()


goodproxies = proxysession.query(Proxys).filter(Proxys.canreachsite == True).filter(Proxys.google == True).all()



results = []


for _ in range(0, 1500):

    print("getting app ids")
    crawls = (session
            .query(Appurl)
            .order_by(Appurl.lastplaycrawl)
            .limit(100)
            .all()
        )

    print("clawling app ids")
    for crawl in crawls:
        result = crawlapage(crawl)
        crawl.lastplaycrawl = datetime.now()
        if result:
            results.append((result, crawl))
            print(f"{crawl.appid} = Good")
        else:
            print(f"{crawl.appid} = No good !")
        time.sleep(1.5)


    print("crawl done, processing results")
    for result in results:
        process_results(result)

    results = []
    print("commiting!")
    session.commit()
