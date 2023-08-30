from models import Appurl, Playstoreapp
from common import make_session
from sqlalchemy import func

session = make_session()

appurls = session.query(Playstoreapp).group_by(Playstoreapp.appid).having(func.count(Playstoreapp.appid) > 1).all()

# print(appurls.statement.compile(compile_kwargs={"literal_binds": True}))

print(appurls)
for app in appurls:
    session.delete(app)
    session.commit()
