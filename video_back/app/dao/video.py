import easyapi
import app.db as db


class VideoDao(easyapi.BusinessBaseDao):
    __tablename__ = 'videos'
    __db__ = db.mysql_db


class WatermarkLogDao(easyapi.BusinessBaseDao):
    __tablename__ = 'watermark_logs'
    __db__ = db.mysql_db

class DownloadLogDao(easyapi.BusinessBaseDao):
    __tablename__ = 'download_logs'
    __db__ = db.mysql_db