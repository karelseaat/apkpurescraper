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

def make_session():
    engine = create_engine("sqlite:///testit.sqlite", echo=False, connect_args={'check_same_thread': False})
    dbsession = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    return dbsession()

session = make_session()
options = Options()
# options.add_argument("--headless")



def crawlapage(page):

    driver.get(page)

    klont = driver.find_elements(By.XPATH, '//a')
    for element in klont:
        thehref = str(element.get_attribute('href'))
        thesplit = thehref.split("/")

        if re.search("^.*\..*\/*.\/.*\..*\.[a-zA-Z0-9]*$", thehref) and len(thesplit) == 5:
            print( thehref)
            if not session.query(Appurl).filter_by(url=thehref).first():
                anewurl = Appurl()
                anewurl.url = thehref
                session.add(anewurl)

    session.commit()


driver = webdriver.Firefox(
    executable_path= r"./geckodriver", options=options
)

crawlapage("https://apkpure.com/2ndline-second-phone-number/com.enflick.android.tn2ndLine")

for crawl in session.query(Appurl).filter_by(done=False).all():
    # print(crawl)
    crawl.done = True
    crawlapage(crawl.url)

    session.add(crawl)
    session.commit()


driver.quit()
