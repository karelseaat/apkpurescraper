#!./venv/bin/python3

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
from fastcrc import crc64

from common import make_session

def generate_stadard_pages(number):
    defurl = "https://apkpure.com/"
    pages = [f"{defurl}game_action?page={x}&sort=new" for x in range(1, number+1)]
    pages += [f"{defurl}game_adventure?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_board?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_card?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_casino?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_casual?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_educational?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_music?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_puzzle?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_racing?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_role_playing?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_simulation?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_sports?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_strategy?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_trivia?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_word?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}game_family?page={x}&sort=new" for x in range(1, number+1)]

    pages +=[f"{defurl}art_and_design?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}auto_and_vihicles?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}beauty?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}books_and_reference?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}business?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}comics?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}comunication?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}dating?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}education?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}entertainment?page={x}&sort=new" for x in range(1, number+1)]

    pages +=[f"{defurl}events?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}finance?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}food_and_drink?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}health_and_fitness?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}house_and_home?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}libraries_and_demo?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}lifestyle?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}maps_and_navigation?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}music_and_audio?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}news_and_magazines?page={x}&sort=new" for x in range(1, number+1)]

    pages +=[f"{defurl}parenting?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}personalization?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}photography?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}productivity?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}shopping?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}social?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}sports?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}tools?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}travel_and_local?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}video_players?page={x}&sort=new" for x in range(1, number+1)]
    pages +=[f"{defurl}weather?page={x}&sort=new" for x in range(1, number+1)]
    return pages

def generate_fdroid_pages(number):
    defurl  = "https://f-droid.org/en/"
    pages = [f"{defurl}categories/connectivity/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/development/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/games/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/graphics/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/internet/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/money/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/multymedia/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/navigation/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/phone-sms/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/reading/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/science-education/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/security/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/sports-health/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/system/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/theming/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/time/{x}/index.html" for x in range(2, number+2)]
    pages += [f"{defurl}categories/writing/{x}/index.html" for x in range(2, number+2)]
    return pages

def generate_brain_pages(number):
    defurl = "https://www.appbrain.com/apps/"
    pages = [f"{defurl}hot/?o={x}" for x in range(0, number+1)]
    pages += [f"{defurl}hot/apps/updated/?o={x}" for x in range(0, number+1)]
    pages += [f"{defurl}hot/apps/new/?o={x}" for x in range(0, number+1)]

    return pages


def integrate(listofapps):
    for app in listofapps:
        session.add(app)
        allids.add(app.appid)

    session.commit()


def run(page):
    driver.get(page)
    appurls = []

    klont = driver.find_elements(By.XPATH, '//a')
    for element in klont:

        try:
            thehref = str(element.get_attribute('href'))
            thesplit = thehref.split("/")
        except Exception as e:
            thesplit = "0"
            thehref = ""

        if re.search("^.*\..*\/*.\/.*\..*\.[a-zA-Z0-9]*$", thehref) and len(thesplit) == 5:

            appid = thehref.split("/")[-1]
            
            if not crc64.ecma_182(appid.encode()) in allids and len(appid) < 128:
                anewurl = Appurl()
                appurls.append(anewurl)
                allids.add(crc64.ecma_182(appid.encode()))
                anewurl.appurl = thehref
                anewurl.appid = appid
    return appurls

def alt_run(page):
    driver.get(page)
    appurls = []

    klont = driver.find_elements(By.XPATH, '//a')
    for element in klont:
        try:
            thehref = str(element.get_attribute('href'))
            thesplit = thehref.split("/")
        except Exception as e:
            thesplit = "0"
            thehref = ""
        
        if len(thesplit) == 7 and re.search("^.*\..*\..*$", thesplit[5]):

            appid = thesplit[5]
            if not crc64.ecma_182(appid.encode()) in allids and len(appid) < 128:

                anewurl = Appurl()
                appurls.append(anewurl)
                allids.add(crc64.ecma_182(appid.encode()))
                anewurl.appurl = thehref
                anewurl.appid = appid


    return appurls


def brain_run(page):
    driver.get(page)
    appurls = []

    klont = driver.find_elements(By.XPATH, '//a')
    for element in klont:
        try:
            thehref = str(element.get_attribute('href'))
            thesplit = thehref.split("/")
        except Exception as e:
            thesplit = "0"
            thehref = ""
        
        
        if len(thesplit) == 6 and re.search("^.*\..*\..*$", thesplit[5]):

            appid = thesplit[5]
            if not crc64.ecma_182(appid.encode()) in allids and len(appid) < 128:

                anewurl = Appurl()
                appurls.append(anewurl)
                allids.add(crc64.ecma_182(appid.encode()))
                anewurl.appurl = thehref
                anewurl.appid = appid

    return appurls

session = make_session()
options = Options()

options.add_argument("--headless")
options.add_argument('--blink-settings=imagesEnabled=false')

options.set_preference("permissions.default.image", 2)
driver = webdriver.Firefox(
    options=options
)

appurls = session.query(Appurl).all()
allids = set([crc64.ecma_182(appurl.appid.encode()) for appurl in appurls])

allapps = []

for app in generate_stadard_pages(2):
    temp = run(app)
    allapps += temp

print(f"num of standard: {len(temp)}")

for app in generate_fdroid_pages(10):
    temp = alt_run(app)
    allapps += temp

print(f"num of froid: {len(temp)}")

for app in generate_brain_pages(10):
    temp = brain_run(app)
    allapps += temp

print(f"num of brain: {len(temp)}")

integrate(allapps)

driver.quit()
