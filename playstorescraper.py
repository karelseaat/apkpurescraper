#!./venv/bin/python3


from models import Playstoreapp, Genre, Developer, Newappurl

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
import time

from datetime import datetime, timedelta
from google_play_scraper import app
import random
from google_play_scraper.features.app import parse_dom
import requests
from common import make_session

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

    thedeveloper = session.query(Developer).filter(Developer.name == result['developer']).first()
    if not thedeveloper:
        thedeveloper = Developer()
    thedeveloper.name = result['developer']
    if result['developerAddress']:
        thedeveloper.address = result['developerAddress'][:127]

    if thedeveloper.name:
        playstoreapp.thedeveloper = thedeveloper
    if result['developerWebsite']:
        playstoreapp.devwebsite = result['developerWebsite']
    playstoreapp.appid = result['appId']
    playstoreapp.downloads = result['minInstalls']
    if result['score']:
        playstoreapp.rating = result['score'] * 10000000
    playstoreapp.reviews = result['reviews']
    if result['video']:
        playstoreapp.hasvideo = True
    playstoreapp.adds = result['adSupported']
    playstoreapp.title = result['title']
    playstoreapp.inapp = result['offersIAP']
    playstoreapp.icon = result['icon']


    genre = session.query(Genre).filter(Genre.name == result['genre']).first()
    if not genre:
        genre = Genre()
        genre.name = result['genre']

    if genre.name:
        playstoreapp.genres.append(genre)

    if result['released']:
        playstoreapp.releasedon = datetime.strptime(result['released'], '%b %d, %Y')

    if result['updated']:
        playstoreapp.lastupdate = datetime.fromtimestamp(int(result['updated']))

    if result['description']:
        playstoreapp.about = result['description'][:255]

    if result['price']:
        playstoreapp.price = result['price']*100
    else:
        playstoreapp.price = 0

    playstoreapp.removedfromstore = False

    session.add(playstoreapp)


def get_raw(url):

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

    page.lastplaycrawl = datetime.now()

    session.add(page)

    url = f"https://play.google.com/store/apps/details?id={page.appid}"
    result = get_raw(url)

    if result[0]:
        return parse_dom(result[1].text, page.appid, url)
    elif result[1] == 2:
        return None
    else:
        return None




session = make_session()

results = []

while True:

    print("getting app ids")
    crawls = (session
            .query(Newappurl)
            .filter(Newappurl.id % 2 == 0)
            .order_by(Newappurl.lastplaycrawl)
            .limit(500)
            .all()
        )

    print("clawling app ids")
    for crawl in crawls:
        result = crawlapage(crawl)
        if result:
            crawl.lastplaycrawl = datetime.now()
            results.append((result, crawl))
            print(f"{crawl.appid} = Good")
        else:

            playstoreapp = session.query(Playstoreapp).filter(Playstoreapp.appid == crawl.appid).first()
            if playstoreapp:
                playstoreapp.removedfromstore = True
            session.delete(crawl)
            print(f"{crawl.appid} = No good !")
        time.sleep(1)


    print("crawl done, processing results")
    for result in results:
        process_results(result)

    results = []
    print("commiting!")
    session.commit()
