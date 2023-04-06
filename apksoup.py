#!/usr/bin/env python

import re

from models import Appurl

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
import time
from datetime import datetime
import threading
from sqlalchemy import func
import requests
from bs4 import BeautifulSoup


def make_session():
    engine = create_engine("mysql+pymysql://root:password@localhost/test?charset=utf8mb4", echo=False)
    dbsession = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return dbsession()


def integrate(listofapps):
    integratecount = 0
    for app in listofapps:

        if not app.appid in allids:
            integratecount += 1
            session.add(app)
            allids.add(app.appid)

    session.commit()
    return integratecount


class myThread (threading.Thread):

    def __init__(self, page):
        super(myThread, self).__init__()
        self.page = page
        self.value = []


    def run(self):

        try:
            r = requests.get(f"https://apksos.com/app/{self.page.appid}", timeout=3)
        except Exception as e:
            print("time out!")
            return


        appurls = []
        soup = BeautifulSoup(r.content, 'html5lib')

        for element in soup.find_all('a', href=True):


            thesplit = element['href'].split("/")


            if re.search("^.*\..*\/*.\/.*\..*\.[a-zA-Z0-9]*$", element['href']) and len(thesplit) == 5 and 'http' in element['href']:

                appid = thesplit[-1]

                if len(appid) < 128:

                    anewurl = Appurl()
                    appurls.append(anewurl)
                    anewurl.appurl = element['href']
                    anewurl.appid = appid

        self.value = appurls

session = make_session()

appurls = session.query(Appurl).all()

allids = set([appurl.appid for appurl in appurls])


threads = []
limits = 4




while True:
    nowtime = datetime.now()
    results = session.query(Appurl).filter_by(done=False).order_by(func.random()).limit(limits).all()
    latertime = datetime.now()

    print("query time: " + str((latertime-nowtime).total_seconds()))

    nowtime = datetime.now()
    for index, result in enumerate(results):
        result.done = True
        session.add(result)
        thread = myThread(result)
        threads.append(thread)
        thread.start()


    latertime = datetime.now()
    print("thread start time: " + str((latertime-nowtime).total_seconds()))
    allresults = []

    nowtime = datetime.now()
    for t in threads:
        t.join()
        allresults += t.value

    latertime = datetime.now()

    print("join seconds: " + str((latertime-nowtime).total_seconds()), " total rsults: " + str(integrate(allresults)))

    nowtime = datetime.now()
    session.commit()
    latertime = datetime.now()
    print("commit time: " + str((latertime-nowtime).total_seconds()))
