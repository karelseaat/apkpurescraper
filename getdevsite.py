#!./venv/bin/python3


import re

from models import Appurl, Developer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
import time
from datetime import datetime
from fastcrc import crc64

from common import make_session
import requests
from bs4 import BeautifulSoup

from urllib.parse import urlparse


session = make_session()

print("getting unique ids")
appurls = session.query(Appurl).all()
allids = set([crc64.ecma_182(appurl.appid.encode()) for appurl in appurls])
print("got unique ids")

def get_all_urls(adev):
        allurls = []
        try:
            result = requests.get(dev.devwebsite, timeout=5)
            if result.status_code == 200:
            
                soup = BeautifulSoup(result.text, 'html.parser')
                parsers = [urlparse(a.get('href')) for a in soup.find_all('a') if a.get('href')]
                for parser in parsers:
                    bleps = [parameter for parameter in parser.query.split("&") ]    
                    for blep in bleps:
                        if "id" in blep and "." in blep and len(blep) < 133 and "https" not in blep:
                            allurls.append(blep.split("=")[-1])
        except Exception:
            pass
        return allurls



while True:
    devstocrawl = session.query(Developer).filter(Developer.devwebsite.isnot(None)).order_by(Developer.crawledat).limit(100).all()
    for dev in devstocrawl:
        appids = get_all_urls(dev)
        
        dev.crawledat = datetime.now()
        for app in appids:
            crced = crc64.ecma_182(app.encode())
            if crced not in allids:
                print(app)
                allids.add(crced)
                newapp = Appurl()
                newapp.appid = app
                session.add(newapp)


                

    session.commit()
