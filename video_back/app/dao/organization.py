import easyapi
import app.db as db

class OrganizationDao(easyapi.BusinessBaseDao):
    __tablename__ = 'organizations'
    __db__ = db.mysql_db


class DistributeVideoDao(easyapi.BusinessBaseDao):
    __tablename__ = 'distribut_videos'
    __db__ = db.mysql_db