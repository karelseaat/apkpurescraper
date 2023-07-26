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
from fastcrc import crc64


def make_session():
    engine = create_engine("mysql+pymysql://root:kateobele@localhost/apkscraper?charset=utf8mb4", echo=False)
    dbsession = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return dbsession()

def split_it(aarray, maxsize):
    return [aarray[i*maxsize:(i+1)*maxsize] for i in range(len(aarray)//maxsize)]

def integrate(listofapps):
    integratecount = 0
    for app in listofapps:

        if not crc64.ecma_182(app.appid.encode()) in allids:
            integratecount += 1
            session.add(app)
            allids.add(crc64.ecma_182(app.appid.encode()))

    # session.commit()
    return integratecount


class myThread (threading.Thread):

    def __init__(self, page):
        super(myThread, self).__init__()
        self.page = page
        self.value = []


    def run(self):

        try:
            r = requests.get(f"https://apksos.com/app/{self.page.appid}", timeout=10)
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

allids = set([crc64.ecma_182(appurl.appid.encode()) for appurl in appurls])


threads = []
limits = 4


while True:
    nowtime = datetime.now()
    results = session.query(Appurl).filter(Appurl.done.is_(None)).order_by(func.random()).limit(40).all()
    latertime = datetime.now()

    print("query time: " + str((latertime-nowtime).total_seconds()))

    nowtime = datetime.now()

    for subarray in split_it(results, limits):
        for index, result in enumerate(subarray):
            result.done = datetime.now()
            session.add(result)
            thread = myThread(result)
            threads.append(thread)
            thread.start()


        allresults = []

        nowtime = datetime.now()
        for t in threads:
            t.join()
            allresults += t.value

        latertime = datetime.now()

        print("join seconds: " + str((latertime-nowtime).total_seconds()), " total rsults: " + str(integrate(allresults)))
        time.sleep(10)

    nowtime = datetime.now()
    session.commit()
    latertime = datetime.now()
    print("commit time: " + str((latertime-nowtime).total_seconds()))
