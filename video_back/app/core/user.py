import easyapi
import app.dao as dao

ctx = easyapi.EasyApiContext()

class UserController(easyapi.BaseController):
    __dao__ = dao.UserDao



    # @classmethod
    # def formatter(cls, data: dict):
    #     new_data = dict()
    #     for key, value in data.items():
    #         if key != "password_hash":
    #             new_data[key] = value
    #     return new_data
    #
    # @classmethod
    # def reformatter(cls, data: dict):
    #     new_data = dict()
    #     for key, value in data.items():
    #         if key != "password_hash" and key != "password":
    #             new_data[key] = value
    #     return new_data


class AdminController(easyapi.BaseController):
    __dao__ = dao.AdminDao