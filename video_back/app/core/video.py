import easyapi
import app.dao as dao
import datetime

class VideoController(easyapi.BaseController):
    __dao__ = dao.VideoDao

    # @classmethod
    # def get(cls, id: int, ctx = None, *args, **kwargs):
    #     res = super.get(id)
    #     if res is None:
    #         return None
    #     return res

class WatermarkLogController(easyapi.BaseController):
    __dao__ = dao.WatermarkLogDao




class DownloadLogController(easyapi.BaseController):
    __dao__ = dao.DownloadLogDao