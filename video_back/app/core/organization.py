import easyapi
import app.dao as dao
from easyapi.sql import Pager, Sorter
from easyapi import EasyApiContext

class OrganizationController(easyapi.BaseController):
    __dao__ = dao.OrganizationDao

    @classmethod
    def get(cls, id: int, ctx: EasyApiContext = None):
        res = super().get(id)
        if res is None:
            return None
        # 添加 father_organization 对象:
            father_organization_id = res['father_organization_id']
        father_organization = dao.OrganizationDao.get(ctx=ctx, query={"id": father_organization_id})
        if father_organization is None:
            father_organization = {}
        res['father_organization'] = father_organization
        return res

    @classmethod
    def query(cls, ctx: EasyApiContext = None, query: dict = None, pager: Pager = None, sorter: Sorter = None, *args,
              **kwargs) -> (list, int):
        (res, total) = super().query(ctx=ctx, query=query, pager=pager, sorter=sorter)
        for res_data in res:
            # 添加 father_organization 对象:
            father_organization_id = res_data['father_organization_id']
            if father_organization_id < 1:
                father_organization = {}
            else:
                father_organization = dao.OrganizationDao.get(ctx=ctx, query={'id': father_organization_id})
                if father_organization is None:
                    # raise easyapi.BusinessError(code=404, http_code=404, err_info="organization not found")
                    father_organization = {}
            res_data['father_organization'] = father_organization
        return res, total


class DistributeVideoController(easyapi.BaseController):
    __dao__ = dao.DistributeVideoDao

    @classmethod
    def get(cls, id: int, ctx: EasyApiContext = None):
        res = super().get(id)
        if res is None:
            return None
        #添加video对象:
        video_id = res['video_id']
        video = dao.VideoDao.get(ctx=ctx, query={"id": video_id})
        if video is None:
            video = {}
        res['video'] = video
        #添加organization对象:
        organization_id = res['organization_id']
        organization = dao.OrganizationDao.get(ctx=ctx,query={"id":organization_id})
        if organization is None:
            organization = {}
        res['organization'] = organization
        return res

    @classmethod
    def query(cls, ctx: EasyApiContext = None, query: dict = None, pager: Pager = None, sorter: Sorter = None, *args, **kwargs) -> (list, int):
        (res ,total) = super().query(ctx=ctx, query=query, pager=pager, sorter=sorter)
        for res_data in res:
            # 添加video对象:
            video_id = res_data['video_id']
            video = dao.VideoDao.get(ctx=ctx, query={"id": video_id})
            if video is None:
                video = {}
            res_data['video'] = video
            # 添加organization对象:
            organization_id = res_data['organization_id']
            organization = dao.OrganizationDao.get(ctx=ctx, query={'id': organization_id})
            if organization is None:
                #raise easyapi.BusinessError(code=404, http_code=404, err_info="organization not found")
                organization = {}
            res_data['organization'] = organization
        return res, total
