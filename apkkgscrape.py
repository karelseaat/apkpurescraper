#!./venv/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from sqlalchemy import func

from selenium.webdriver.firefox.options import Options
import re

from models import Appurl


import time
from datetime import datetime, timedelta
import threading

from fastcrc import crc64
from common import make_session

def split_it(aarray, maxsize):
    return [aarray[i*maxsize:(i+1)*maxsize] for i in range(len(aarray)//maxsize)]


def integrate(listofapps):
    integratecount = 0
    for app in listofapps:

        if not crc64.ecma_182(app.appid.encode()) in allids:
            integratecount += 1
            session.add(app)
            allids.add(crc64.ecma_182(app.appid.encode()))

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
                if len(appid) < 128:

                    anewurl = Appurl()
                    appurls.append(anewurl)
                    anewurl.appurl = thehref
                    anewurl.appid = appid

        self.value = appurls


session = make_session()

appurls = session.query(Appurl).all()

allids = set([crc64.ecma_182(appurl.appid.encode()) for appurl in appurls])


threads = []
limits = 10
drivers = []

for i in range(limits):
    print(i)
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Firefox(options=options)
    drivers.append(driver)
    driver.set_page_load_timeout(10)


while True:
    nowtime = datetime.now()
    results = session.query(Appurl).filter(Appurl.done.is_(None)).filter(Appurl.appurl.like('%apkpure.com%')).order_by(func.random()).limit(200).all()
    latertime = datetime.now()

    print("query time: " + str((latertime-nowtime).total_seconds()))

    nowtime = datetime.now()


    for subarray in split_it(results, limits):

        for index, result in enumerate(subarray):
            result.done = datetime.now()
            session.add(result)
            thread = myThread(result, drivers[index])
            threads.append(thread)
            thread.start()


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
