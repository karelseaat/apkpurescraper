#!/home/aat/apkpurescraper/venv/bin/python3

from models import Playstoreapp, Newappurl, Developer, Genre, Keyword
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import func, case, cast, join, Integer, DateTime, TIMESTAMP
from sqlalchemy.orm import sessionmaker, scoped_session
from common import make_session
import datetime
import yake

asession = make_session()

hugelist = []

results = (
    asession.query(Playstoreapp).
    filter(Playstoreapp.default_lang.is_not(None)).
    order_by(Playstoreapp.last_keywording_timestamp).
    limit(100).
    all()
)

if results:
    for result in results:
        if result.about:
            kw_extractor = yake.KeywordExtractor(lan=result.default_lang)
            keywords = [keywordstring[0] for keywordstring in kw_extractor.extract_keywords(result.about.lower()) if float(keywordstring[1]) < 0.1]
            result.last_keywording_timestamp = datetime.datetime.now()
            for keywordobject in result.keywords:
                asession.delete(keywordobject)

            for keyword in keywords:
                newkeyw = Keyword()
                newkeyw.keyname = keyword
                result.keywords.append(newkeyw)
    
    asession.commit()
    asession.close()

