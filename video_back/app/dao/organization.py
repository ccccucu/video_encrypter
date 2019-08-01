import easyapi
import app.db as db

class OrganizationDao(easyapi.BusinessBaseDao):
    __tablename__ = 'organization'
    __db__ = db.mysql_db


class DistributeVideoDao(easyapi.BusinessBaseDao):
    __tablename__ = 'distribute_video'
    __db__ = db.mysql_db