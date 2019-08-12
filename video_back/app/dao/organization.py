import easyapi
import app.db as db
from easyapi.context import EasyApiContext

class OrganizationDao(easyapi.BusinessBaseDao):
    __tablename__ = 'organizations'
    __db__ = db.mysql_db


class DistributeVideoDao(easyapi.BusinessBaseDao):
    __tablename__ = 'distribut_videos'
    __db__ = db.mysql_db

    @classmethod
    def insert(cls, ctx: EasyApiContext = None, data: dict = None, modify_by=''):
        """
        插入 补充modify_by
        :param ctx:
        :param data:
        :param modify_by:
        :return:
        """
        return super().insert(ctx=ctx,data=data,modify_by='管理员')