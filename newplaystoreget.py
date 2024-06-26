#!./venv/bin/python3

import requests
from bs4 import BeautifulSoup
import gzip
from models import Newappurl

from common import make_session
from fastcrc import crc64
import time
import datetime
import random

allcollectionfiles = []
allplaystoreappids = []
allplaystorelinks = set()

result = requests.get("https://play.google.com/robots.txt")

sitemaps = [n for n in result.text.strip("\n").split()[-3:] if "http" in n]

session = make_session()

appurls = session.query(Newappurl).all()

allids = {crc64.ecma_182(appurl.appid.encode()): appurl for appurl in appurls}

for n in sitemaps:
    results = requests.get(n)
    soup = BeautifulSoup(results.text, 'lxml')
    elements = soup.find_all('loc')

    for a in elements:
        allcollectionfiles.append(a.get_text())

listlength = round(len(allcollectionfiles)/4)
random.shuffle(allcollectionfiles)

offset = (datetime.datetime.now().isocalendar()[0]) % 4

oldallidslen = 0

for idx, onecol in enumerate(allcollectionfiles[offset*listlength:(offset+1)*listlength]):
    result = requests.get(onecol)
    try:
        soup = BeautifulSoup(gzip.decompress(result.content), "lxml")
    except Exception:
        soup = BeautifulSoup("", "lxml")

    now = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    print(
        f"index of source list: {idx} of {listlength} uniqe inserted recs: {len(allids)} Date: {now}")
    time.sleep(1)

    tocrawl = soup.find_all('xhtml:link')
    random.shuffle(tocrawl)
    for link in tocrawl:
        temp = link['href']
        if "apps" in temp:
            temp2 = temp.split("/")[-1]
            if "=" in temp2:
                temp3 = temp2.split("=")[-1]
                if crc64.ecma_182(temp3.encode()) not in allids:
                    anewappurl = Newappurl()
                    anewappurl.appid = temp3
                    session.add(anewappurl)
                    allids.update({crc64.ecma_182(temp3.encode()): anewappurl})
    try:
        if len(allids) > oldallidslen:
            print("commiting")
            oldallidslen = len(allids) + 100
            session.commit()
    except:
        print("An exception occurred")
session.commit()
session.close()
