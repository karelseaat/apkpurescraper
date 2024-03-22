#!./venv/bin/python3


from models import Newappurl, Playstoreapp

from sqlalchemy import create_engine
from models import Base
from sqlalchemy import delete

from datetime import datetime, timedelta
from common import make_session

mothsago = datetime.now() - timedelta(30 * 6)
session = make_session()
results = session.query(Newappurl).filter(Newappurl.lastplaycrawl < mothsago).limit(10000).all()

appids = [result.appid for result in results]

for result in results:
    session.delete(result)

print(appids)

results = session.query(Playstoreapp).where(Playstoreapp.appid.in_(appids)).all()
for result in results:
    result.removedfromstore = True

session.commit()

session.close()
