#!/home/aat/apkpurescraper/venv/bin/python3

from models import Playstoreapp, Newappurl, Developer, Genre
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import func, case, cast, join, Integer, DateTime, TIMESTAMP
from sqlalchemy.orm import sessionmaker, scoped_session
from common import make_session
import datetime
from collections import Counter
import yake
from collections import Counter

asession = make_session()

hugelist = []

results = (
    asession.query(Playstoreapp).
    filter(Playstoreapp.default_lang.is_not(None)).
    order_by(Playstoreapp.last_classify_timestamp).
    limit(100000).
    all()
)

if results:
    for result in results:
        if result.about:
            kw_extractor = yake.KeywordExtractor(lan=result.default_lang)
            keywords = kw_extractor.extract_keywords(result.about.lower())
            goodkeywords = [keyword[0] for keyword in keywords if keyword[1] < 0.05]
            hugelist.extend(goodkeywords)
        result.keywords_timestamp = datetime.datetime.now()

print(Counter(hugelist))
