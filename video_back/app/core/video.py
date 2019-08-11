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
from easyapi.sql import Pager, Sorter
from easyapi import EasyApiContext
from datetime import datetime, timedelta
from flask_jwt import jwt_required, current_identity

class VideoController(easyapi.BaseController):
    __dao__ = dao.VideoDao

    @classmethod
    def get(cls, id: int, ctx: EasyApiContext = None):
        res = super().get(id)
        if res is None:
            return None

        # 添加upload_organization对象:
        upload_organization_id = res['upload_organization_id']
        upload_organization = dao.OrganizationDao.get(ctx=ctx, query={"id": upload_organization_id})
        if upload_organization is None:
            upload_organization = {}
        res['upload_organization'] = upload_organization

        # 添加upload_admin对象:
        upload_admin_id = res['upload_admin_id']
        upload_admin = dao.UserDao.get(ctx=ctx, query={"id": upload_admin_id})
        if upload_admin is None:
            upload_admin = {}
        res['upload_admin'] = upload_admin

        # 添加release_admin对象:
        release_admin_id = res['release_admin_id']
        release_admin = dao.UserDao.get(ctx=ctx, query={"id": release_admin_id})
        if release_admin is None:
            release_admin = {}
        res['release_admin'] = release_admin

        # 添加delete_admin对象:
        delete_admin_id = res['delete_admin_id']
        delete_admin = dao.UserDao.get(ctx=ctx, query={"id": delete_admin_id})
        if delete_admin is None:
            delete_admin = {}
        res['delete_admin'] = delete_admin

        return res

    @classmethod
    def query(cls, ctx: EasyApiContext = None, query: dict = None, pager: Pager = None, sorter: Sorter = None, *args,
              **kwargs) -> (list, int):
        (res, total) = super().query(ctx=ctx, query=query, pager=pager, sorter=sorter)
        for res_data in res:

            # 添加upload_organization对象:
            upload_organization_id = res_data['upload_organization_id']
            upload_organization = dao.OrganizationDao.get(ctx=ctx, query={"id": upload_organization_id})
            if upload_organization is None:
                upload_organization = {}
            res_data['upload_organization'] = upload_organization

            # 添加upload_admin对象:
            upload_admin_id = res_data['upload_admin_id']
            upload_admin = dao.UserDao.get(ctx=ctx, query={"id": upload_admin_id})
            if upload_admin is None:
                upload_admin = {}
            res_data['upload_admin'] = upload_admin

            # 添加release_admin对象:
            release_admin_id = res_data['release_admin_id']
            release_admin = dao.UserDao.get(ctx=ctx, query={"id": release_admin_id})
            if release_admin is None:
                release_admin = {}
            res_data['release_admin'] = release_admin

            # 添加delete_admin对象:
            delete_admin_id = res_data['delete_admin_id']
            delete_admin = dao.UserDao.get(ctx=ctx, query={"id": delete_admin_id})
            if delete_admin is None:
                delete_admin = {}
            res_data['delete_admin'] = delete_admin

        return res, total


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
        #res = 0
        if res > 0:
            raise easyapi.BusinessError(code=500, http_code=200, err_info="加密失败")

        video_id = dao.VideoDao.insert(ctx=easyapi.EasyApiContext(),
                                       data={"title": title,
                                             "uuid": uuid_1,
                                             "upload_organization_id": 1,
                                             "upload_admin_id": 1,
                                             "allow_play_time": datetime.now(),
                                             "original_file_size": original_file_size,
                                             "release_allow": 1,
                                             "release_admin_id": 1,
                                             "release_time": datetime.now(),
                                             "secret_key": key
                                             })
        return video_id

    @classmethod
    def query_distribute_videos(cls, query, pager, sorter, current_user):
        """
        获取分发给本人的视频
        :param user:
        :return:
        """
        ctx = easyapi.EasyApiContext()
        distributes = dao.DistributeVideoDao.query(ctx=ctx,
                                                   query={'organization_id': current_user.get('organization_id', 1)},
                                                   pager=None,
                                                   sorter=None)
        if not distributes:
            return [], 0
        return super().query(ctx=ctx,
                             query={**query,
                                    '_in_id': [d.get('video_id') for d in distributes]
                                    },
                             pager=pager,
                             sorter=sorter)


class WatermarkLogController(easyapi.BaseController):
    __dao__ = dao.WatermarkLogDao

    @classmethod
    def get(cls, id: int, ctx: EasyApiContext = None):
        res = super().get(id)
        if res is None:
            return None

        # 添加video对象:
        video_id = res['video_id']
        video = dao.VideoDao.get(ctx=ctx, query={"id": video_id})
        if video is None:
            video = {}
        res['video'] = video

        # 添加organization对象
        organization_id = res['organization_id']
        organization = dao.OrganizationDao.get(ctx=ctx, query={"id": organization_id})
        if organization is None:
            organization = {}
        res['organization'] = organization

        # 添加user对象
        user_id = res['user_id']
        user = dao.UserDao.get(ctx=ctx, query={"id": user_id})
        if user is None:
            user = {}
        res['user'] = user

        return res

    @classmethod
    def query(cls, ctx: EasyApiContext = None, query: dict = None, pager: Pager = None, sorter: Sorter = None, *args,
              **kwargs) -> (list, int):
        (res, total) = super().query(ctx=ctx, query=query, pager=pager, sorter=sorter)
        for res_data in res:

            # 添加video对象:
            video_id = res_data['video_id']
            video = dao.VideoDao.get(ctx=ctx, query={"id": video_id})
            if video is None:
                video = {}
            res_data['video'] = video

            # 添加organization对象
            organization_id = res_data['organization_id']
            organization = dao.OrganizationDao.get(ctx=ctx, query={"id": organization_id})
            if organization is None:
                organization = {}
            res_data['organization'] = organization

            # 添加user对象
            user_id = res_data['user_id']
            user = dao.UserDao.get(ctx=ctx, query={"id": user_id})
            if user is None:
                user = {}
            res_data['user'] = user

        return res, total


class DownloadLogController(easyapi.BaseController):
    __dao__ = dao.DownloadLogDao

    @classmethod
    def get(cls, id: int, ctx: EasyApiContext = None):
        res = super().get(id)
        if res is None:
            return None

        # 添加video对象:
        video_id = res['video_id']
        video = dao.VideoDao.get(ctx=ctx, query={"id": video_id})
        if video is None:
            video = {}
        res['video'] = video

        # 添加organization对象
        organization_id = res['organization_id']
        organization = dao.OrganizationDao.get(ctx=ctx, query={"id": organization_id})
        if organization is None:
            organization = {}
        res['organization'] = organization

        # 添加 download_user 对象
        download_user_id = res['download_user_id']
        download_user = dao.UserDao.get(ctx=ctx, query={"id": download_user_id})
        if download_user is None:
            download_user = {}
        res['download_user'] = download_user

        return res

    @classmethod
    def query(cls, ctx: EasyApiContext = None, query: dict = None, pager: Pager = None, sorter: Sorter = None, *args,
              **kwargs) -> (list, int):
        (res, total) = super().query(ctx=ctx, query=query, pager=pager, sorter=sorter)
        for res_data in res:

            # 添加video对象:
            video_id = res_data['video_id']
            video = dao.VideoDao.get(ctx=ctx, query={"id": video_id})
            if video is None:
                video = {}
            res_data['video'] = video

            # 添加organization对象
            organization_id = res_data['organization_id']
            organization = dao.OrganizationDao.get(ctx=ctx, query={"id": organization_id})
            if organization is None:
                organization = {}
            res_data['organization'] = organization

            # 添加 download_user 对象
            download_user_id = res_data['download_user_id']
            download_user = dao.UserDao.get(ctx=ctx, query={"id": download_user_id})
            if download_user is None:
                download_user = {}
            res_data['download_user'] = download_user

        return res, total