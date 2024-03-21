#!./venv/bin/python3


from models import Newappurl

from sqlalchemy import create_engine
from models import Base
from sqlalchemy import delete

from datetime import datetime, timedelta
from common import make_session

mothsago = datetime.now() - timedelta(30 * 6)

session = make_session()
results = session.query(Newappurl).filter(Newappurl.lastplaycrawl < mothsago).all()

for result in results:
    result.delete()

session.commit()

session.close()
