#!./venv/bin/python3

from sqlalchemy.sql import exists
from models import Newappurl, Playstoreapp

from sqlalchemy import create_engine
from models import Base
from sqlalchemy import delete

from datetime import datetime, timedelta
from common import make_session
import random


session = make_session()

mothsago = datetime.now() - timedelta(30 * 6)
results = session.query(Newappurl).filter(Newappurl.lastplaycrawl < mothsago).limit(10000).all()

appids = [result.appid for result in results]

for result in results:
    session.delete(result)


results = session.query(Playstoreapp).where(Playstoreapp.appid.in_(appids)).all()
for result in results:
    result.removedfromstore = True

session.commit()
session.close()

session = make_session()
#------------------------------------
subquerry = session.query(Newappurl.appid)
q = session.query(Playstoreapp).filter(Playstoreapp.appid.not_in(subquerry)).filter(Playstoreapp.removedfromstore == False).delete()
    

print(q)

session.close()
