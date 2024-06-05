
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


thingstodo = True

offset = 0
batch_size = 1000

while thingstodo:

    results = (
        asession.query(Playstoreapp).
        order_by(Playstoreapp.last_classify_timestamp).
        limit(batch_size).
        offset(offset).
        all()
    )

    offset += batch_size
    if results:
        for result in results:
            result.default_lang = langid.classify(result.about)[0]
            result.last_classify_timestamp = datetime.datetime.now()
    else:
        thingstodo = False

    asession.commit()

asession.close()
