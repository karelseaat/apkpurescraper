from models import Appurl, Playstoreapp, Developer
from common import make_session


session = make_session()

appurls = session.query(Playstoreapp).where(Playstoreapp.developer != None).limit(100000).all()

for app in appurls:
    adeveloper = session.query(Developer).where(Developer.name == app.developer).first()
    if not adeveloper:
        adeveloper = Developer()
    adeveloper.name = app.developer
    adeveloper.devwebsite = app.devwebsite
    adeveloper.address = app.address
    app.thedveloper = adeveloper
    app.developer = None
    app.devwebsite = None
    app.address = None
    app.thedeveloper = adeveloper

session.commit()
