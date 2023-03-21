#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.options import Options
import re

from models import Appurl

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
import time
from datetime import datetime
import threading
from sqlalchemy import func


def make_session():
    engine = create_engine("sqlite:///testit.sqlite", echo=False, connect_args={'check_same_thread': False})
    dbsession = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return dbsession()

session = make_session()


appurls = session.query(Appurl).all()

allids = set([appurl.appid for appurl in appurls])

def integrate(listofapps):
    integratecount = 0
    for app in listofapps:

        if not app.appid in allids:
            integratecount += 1
            session.add(app)
            allids.add(app.appid)

    return integratecount

class myThread (threading.Thread):

    def __init__(self, page, driver):
        super(myThread, self).__init__()
        self.page = page
        self.value = []
        self.driver = driver

    def run(self):
        self.driver.get(self.page.appurl)
        appurls = []

        klont = self.driver.find_elements(By.XPATH, '//a')
        for element in klont:
            thehref = str(element.get_attribute('href'))
            thesplit = thehref.split("/")

            if re.search("^.*\..*\/*.\/.*\..*\.[a-zA-Z0-9]*$", thehref) and len(thesplit) == 5:

                appid = thehref.split("/")[-1]

                anewurl = Appurl()
                appurls.append(anewurl)
                anewurl.appurl = thehref
                anewurl.appid = appid

        self.value = appurls


threads = []
limits = 2
drivers = []

for i in range(limits):
    print(i)
    options = Options()
    options.add_argument("--headless")
    drivers.append(webdriver.Firefox(executable_path= r"./geckodriver", options=options))


while True:
    nowtime = datetime.now()
    results = session.query(Appurl).filter_by(done=False).filter(Appurl.appurl.like("https://apkpure.com/%")).order_by(func.random()).limit(limits).all()
    latertime = datetime.now()

    print("query time: " + str((latertime-nowtime).total_seconds()))

    nowtime = datetime.now()
    for index, result in enumerate(results):
        result.done = True
        session.add(result)
        thread = myThread(result, drivers[index])
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


    session.commit()
