import easyapi
import app.dao as dao
from easyapi.sql import Pager, Sorter
from easyapi import EasyApiContext

ctx = easyapi.EasyApiContext()

class UserController(easyapi.BaseController):
    __dao__ = dao.UserDao

    #formatter是out   reformatter是in 进入db
    @classmethod
    def formatter(cls, ctx: EasyApiContext , data: dict):
        new_data = dict()
        for key, value in data.items():
            if key != "password":
                new_data[key] = value
        return new_data

    @classmethod
    def get(cls, id: int, ctx: EasyApiContext = None):
        res = super().get(id)
        if res is None:
            return None
        #添加organization对象
        organization_id = res['organization_id']
        organization = dao.OrganizationDao.get(ctx=ctx,query={"id":organization_id})
        if organization is None:
            organization = {}
        res['organization'] = organization
        return res

    @classmethod
    def query(cls, ctx: EasyApiContext = None, query: dict = None, pager: Pager = None, sorter: Sorter = None, *args, **kwargs) -> (list, int):
        (res, total) = super().query(ctx=ctx, query=query, pager=pager, sorter=sorter)
        # 添加organization对象
        for res_data in res:
            organization_id = res_data['organization_id']
            organization = dao.OrganizationDao.get(ctx=ctx, query={'id': organization_id})
            if organization is None:
                # raise easyapi.BusinessError(code=404, http_code=404, err_info="organization not found")
                organization = {}
            res_data['organization'] = organization
        return res, total


class AdminController(easyapi.BaseController):
    __dao__ = dao.AdminDao

    # formatter是out   reformatter是in 进入db
    @classmethod
    def formatter(cls, ctx: EasyApiContext, data: dict):
        new_data = dict()
        for key, value in data.items():
            if key != "password":
                new_data[key] = value
        return new_data

    @classmethod
    def get(cls, id: int, ctx: EasyApiContext = None):
        res = super().get(id)
        if res is None:
            return None
        #添加organization对象
        organization_id = res['organization_id']
        organization = dao.OrganizationDao.get(ctx=ctx,query={"id":organization_id})
        if organization is None:
            organization = {}
        res['organization'] = organization
        return res

    @classmethod
    def query(cls, ctx: EasyApiContext = None, query: dict = None, pager: Pager = None, sorter: Sorter = None, *args, **kwargs) -> (list, int):
        (res ,total) = super().query(ctx=ctx, query=query, pager=pager, sorter=sorter)
        #添加organization对象
        for res_data in res:
            organization_id = res_data['organization_id']
            organization = dao.OrganizationDao.get(ctx=ctx, query={'id': organization_id})
            if organization is None:
                #raise easyapi.BusinessError(code=404, http_code=404, err_info="organization not found")
                organization = {}
            res_data['organization'] = organization
        return res, total



class LoginLogController(easyapi.BaseController):
    __dao__ = dao.LoginLogDao

    @classmethod
    def get(cls, id: int, ctx: EasyApiContext = None):
        res = super().get(id)
        if res is None:
            return None
        # 添加user or admin对象
        user_id = res['user_id']
        if res['login_role'] == 'admin':
            admin = dao.AdminDao.get(ctx=ctx, query={'id': user_id})
            if admin is None:
                admin = {}
            res['admin'] = admin
        elif res['login_role'] == 'user':
            user = dao.UserDao.get(ctx=ctx, query={'id': user_id})
            if user is None:
                user = {}
            res['user'] = user
        else:
            pass
        return res

    @classmethod
    def query(cls, ctx: EasyApiContext = None, query: dict = None, pager: Pager = None, sorter: Sorter = None, *args, **kwargs) -> (list, int):
        (res, total) = super().query(ctx=ctx, query=query, pager=pager, sorter=sorter)
        # 添加user对象
        for res_data in res:
            user_id = res_data['user_id']
            if res_data['login_role'] == 'admin':
                admin = dao.AdminDao.get(ctx=ctx, query={'id': user_id})
                if admin is None:
                    admin = {}
                res_data['admin'] = admin
            elif res_data['login_role'] == 'user':
                user = dao.UserDao.get(ctx=ctx, query={'id': user_id})
                if user is None:
                    user = {}
                res_data['user'] = user
            else:
                pass
        return res, total