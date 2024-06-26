#!./venv/bin/python3


from models import Playstoreapp, Genre, Developer, Newappurl, Contentrating

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
from config import one_or_zero, batch_size
from urllib.parse import urlparse
import json


def process_results(multy):

    result, page = multy
    playstoreapp = session.query(Playstoreapp).filter(
        Playstoreapp.appid == result['appId']).first()
    if not playstoreapp:
        playstoreapp = Playstoreapp()

    thecontentrating = session.query(Contentrating).filter(
        Contentrating.name == result['contentRating']).first()
    if not thecontentrating:
        thecontentrating = Contentrating()
        thecontentrating.name = result['contentRating']

    playstoreapp.contentrating = thecontentrating

    thedeveloper = session.query(Developer).filter(
        Developer.name == result['developer']).first()
    if not thedeveloper:
        thedeveloper = Developer()
        thedeveloper.name = result['developer']

    if result['developerAddress']:
        thedeveloper.address = result['developerAddress'][:127]

    if result['developerEmail']:
        thedeveloper.email = result['developerEmail']
    if thedeveloper.name:
        playstoreapp.thedeveloper = thedeveloper
    if result['developerWebsite']:
        playstoreapp.devwebsite = result['developerWebsite']
        urlobject = urlparse(result['developerWebsite'])
        thedeveloper.devwebsite = urlobject.hostname
    playstoreapp.appid = result['appId']
    playstoreapp.downloads = result['realInstalls']
    if result['screenshots']:
        playstoreapp.screenshotnum = len(result['screenshots'])
    if result['updated']:
        if not playstoreapp.allupdates:
            playstoreapp.allupdates = [result['updated']]
        elif result['updated'] not in playstoreapp.allupdates:
            playstoreapp.allupdates.append(result['updated'])
    if result['version'] and len(result['version']) < 64:
        playstoreapp.currentversion = result['version']
    if result['privacyPolicy'] and len(result['privacyPolicy']) < 512:
        playstoreapp.privacypolicylink = result['privacyPolicy']
    if result['score']:
        playstoreapp.rating = result['score'] * 10000000
    playstoreapp.reviews = result['reviews']
    if result['video']:
        playstoreapp.hasvideo = True
    if result['summary']:
        playstoreapp.summary = result['summary']
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
        playstoreapp.releasedon = datetime.strptime(
            result['released'], '%b %d, %Y')

    if result['updated']:
        playstoreapp.lastupdate = datetime.fromtimestamp(
            int(result['updated']))

    if result['description']:
        playstoreapp.about = result['description'][:3072]

    if result['price']:
        playstoreapp.price = result['price']*100
    else:
        playstoreapp.price = 0

    playstoreapp.removedfromstore = False
    if not playstoreapp.crawl_counter:
        playstoreapp.crawl_counter = 0
    else:
        playstoreapp.crawl_counter += 1

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
        time.sleep(1000)
        return 0, 2


def crawlapage(page):

    page.lastplaycrawl = datetime.now()

    session.add(page)

    url = f"https://play.google.com/store/apps/details?id={page.appid}"
    result = get_raw(url)

    if result[0]:
        return parse_dom(result[1].text, page.appid, url)
    else:
        return None


session = make_session()

results = []

while True:

    print("getting app ids")
    crawls = (session
              .query(Newappurl)
              .filter(Newappurl.id % 2 == one_or_zero)
              .order_by(Newappurl.lastplaycrawl)
              .limit(batch_size)
              .all()
              )

    print("clawling app ids")
    for crawl in crawls:
        curtime = time.time()
        result = crawlapage(crawl)
        if result:
            crawl.lastplaycrawl = datetime.now()
            results.append((result, crawl))
            timedelta = time.time() - curtime
            print(f"id:{crawl.id} Good      , timedelta = {round(timedelta, 3)}, crawlnumber = {len(crawls)}/{crawls.index(crawl)} appid:{crawl.appid}")
        else:

            playstoreapp = session.query(Playstoreapp).filter(
                Playstoreapp.appid == crawl.appid).first()
            if playstoreapp:
                playstoreapp.removedfromstore = True
            session.delete(crawl)
            timedelta = time.time() - curtime
            print(f"id:{crawl.id} notGood!!!, timedelta = {round(timedelta, 3)}, crawlnumber = {len(crawls)}/{crawls.index(crawl)} appid:{crawl.appid}")
        if timedelta >= 1:
            time.sleep(0.5)
        else:
            time.sleep(1 - timedelta)

    print("crawl done, processing results")
    for result in results:
        process_results(result)

    results = []
    print("commiting!")
    session.commit()
