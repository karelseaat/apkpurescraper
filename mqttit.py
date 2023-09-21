#!./venv/bin/python3

from models import Appurl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
from common import make_session
import paho.mqtt.client as mqtt
from sqlalchemy import func

blaat = client =mqtt.Client("scraperrella")
blaat.connect("test.mosquitto.org", port=1883, keepalive=60, bind_address="")
session = make_session()

results = session.query(Appurl).order_by(func.random()).limit(50).all()
listo = [app.appid for app in results]


blaat.publish("storescraper/scraperrella", ",".join(listo))


