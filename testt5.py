#!/home/aat/androidstoreapi/venv/bin/python3

from models import Playstoreapp, Newappurl, Developer, Genre
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import func, case, cast, join, Integer, DateTime, TIMESTAMP
from sqlalchemy.orm import sessionmaker, scoped_session
from common import make_session
from config import redis_port, redis_host
import redis
import json
from keyphrasetransformer import KeyPhraseTransformer
from pprint import pprint

asession = make_session()

r = redis.Redis(host=redis_host, port=redis_port)

kp = KeyPhraseTransformer()

thingstodo = True

offset = 0

while thingstodo:

    results = (
        asession.query(Playstoreapp.about).
        limit(10).
        offset(offset).
        all()
    )

    offset += 10
    if results:
        for result in results:
            for keyword in kp.get_key_phrases(result[0]):
                r.lpush('testlist', keyword.encode('utf-8'))
    else:
        thingstodo = False

    print(offset)
