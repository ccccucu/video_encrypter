from flask import Flask, Blueprint, jsonify
import easyapi
import app.core as controller
from flask_jwt import current_identity, jwt_required


class UserHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.UserController

user_bp = Blueprint(name='users', import_name='users', url_prefix='')

easyapi.register_api(app=user_bp, view=UserHandler, endpoint='user_api', url='/users')

# 用户登录接口已由flask-jwt默认定义好，默认路由是"/auth"，可以在配置文件中配置:
# JWT_AUTH_URL_RULE = '/login'
# 修改登录接口路由为'/login'
# 需要注意的是，登录接口的传值要使用 application/json 形式


class LoginLogHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.LoginLogController


login_log_bp = Blueprint(name='login_logs', import_name='login_logs', url_prefix='')

easyapi.register_api(app=login_log_bp, view=LoginLogHandler, endpoint='login_log_api', url='/login_logs')