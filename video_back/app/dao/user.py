import easyapi
import app.db as db

from werkzeug.security import generate_password_hash

#用户和管理员都使用这一张表
class UserDao(easyapi.BusinessBaseDao):
    __tablename__ = "users"
    __db__ = db.mysql_db

    # @classmethod
    # def reformatter(cls, ctx = None, data = None, *args, **kwargs):
    #     new_data = dict()
    #     for key,value in data.items():
    #         if key == "password":
    #             # 当前不加密
    #             new_data["password_hash"] = data["password"] # 加密： generate_password_hash(data["password"])
    #         else:
    #             new_data[key] = value
    #     unscoped = data.get('unscoped', False)
    #     if not  unscoped and 'deleted_at' not in data:
    #         new_data['deleted_at'] = None
    #     return new_data


class LoginLogDao(easyapi.BusinessBaseDao):
    __tablename__ = "login_logs"
    __db__ = db.mysql_db

