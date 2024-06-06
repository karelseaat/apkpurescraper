#!/home/aat/apkpurescraper/venv/bin/python3

from models import Playstoreapp, Newappurl, Developer, Genre
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import func, case, cast, join, Integer, DateTime, TIMESTAMP
from sqlalchemy.orm import sessionmaker, scoped_session
from common import make_session
from pprint import pprint
import langid
import datetime

asession = make_session()


for i in range(100):
    results = (
        asession.query(Playstoreapp).
        order_by(Playstoreapp.last_classify_timestamp).
        limit(1000).
        all()
    )

    if results:
        for result in results:
            if result.about:
                result.default_lang = langid.classify(result.about)[0]
            result.last_classify_timestamp = datetime.datetime.now()
    else:
        thingstodo = False

    asession.commit()

asession.close()
