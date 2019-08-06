import os
import easyapi
import random
import uuid
import time
import datetime
from werkzeug.datastructures import FileStorage
from video_sdk import rpc
import app.dao as dao
from app.utils import util


class VideoController(easyapi.BaseController):
    __dao__ = dao.VideoDao

    # @classmethod
    # def get(cls, id: int, ctx = None, *args, **kwargs):
    #     res = super.get(id)
    #     if res is None:
    #         return None
    #     return res

    ALLOW_TYPE = ['video/mp4', 'video/mpeg']

    @classmethod
    def upload_video(cls, file: FileStorage, origin_path: str, encrpty_path: str, thumnail_path: str):
        """
        上传视频并且加密 提取缩略图
        :param file:
        :param origin_path:
        :param encrpty_path:
        :param thumnail_path:
        :return:
        """
        if file.mimetype not in cls.ALLOW_TYPE:
            raise easyapi.BusinessError(code=500, http_code=200, err_info="不是允许的文件")
        title, _ = os.path.splitext(file.filename)
        uuid_1 = str(uuid.uuid1())

        origin_file = os.path.join(origin_path, uuid_1 + '.mp4')
        encrypt_file = os.path.join(encrpty_path, uuid_1 + '.mp4')

        original_file_size = file.content_length
        file.save(origin_file)

        # 加密
        key = util.ranstr(32)
        res = rpc.en_file_by_path(origin_file, key, encrypt_file)
        if res > 0:
            raise easyapi.BusinessError(code=500, http_code=200, err_info="加密失败")

        dao.VideoDao.insert(ctx=easyapi.EasyApiContext(),
                            data={"title": title, "uuid": uuid_1,
                                  "original_file_size": original_file_size,
                                  "allow_play_time": "2019-08-02 16:37:45",
                                  "delete_admin_user_id": 1,
                                  "release_time": "2019-08-02 16:37:45",
                                  "release_admin_user_id": 1,
                                  "upload_admin_user_id": 1,
                                  "upload_organization_id": 1,
                                  "secret_key": key
                                  })

    @classmethod
    def query_distribute_videos(cls, query, pager, sorter, current_user):
        """
        获取分发给本人的视频
        :param user:
        :return:
        """
        ctx = easyapi.EasyApiContext()
        return super().query(ctx=ctx,
                             query={**query, 'organization_id': current_user.get('organization_id', 1)},
                             pager=pager,
                             sorter=sorter)


class WatermarkLogController(easyapi.BaseController):
    __dao__ = dao.WatermarkLogDao


class DownloadLogController(easyapi.BaseController):
    __dao__ = dao.DownloadLogDao
