from models import Appurl, Playstoreapp, Developer
from common import make_session
from sqlalchemy import func

session = make_session()

devs = session.query(Developer).group_by(Developer.name).having(func.count(Developer.name) > 1).all()

# print(appurls.statement.compile(compile_kwargs={"literal_binds": True}))

#print(appurls)
for dev in devs:
    session.delete(dev)
    session.commit()
    print(dev)
