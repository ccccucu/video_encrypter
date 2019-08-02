from flask import Flask, Blueprint, jsonify
import easyapi
import app.core as controller
from flask_jwt import current_identity, jwt_required


class AdminHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.AdminController


admin_bp = Blueprint(name='admins', import_name='admins', url_prefix='')

easyapi.register_api(app=admin_bp, view=AdminHandler, endpoint='admin_api', url='/admins')

@admin_bp.route('/admins/login',methods=['GET','POST'])  #不写,methods=['GET','POST'] 默认是get
def video_upload():
    try:
        pass
    except easyapi.BusinessError as e:
        return jsonify(**{
            'msg': e.err_info,
            'code': e.code,
        }), e.http_code
    return jsonify(code=200, msg='登录成功')








class UserHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.UserController


user_bp = Blueprint(name='users', import_name='users', url_prefix='')

easyapi.register_api(app=user_bp, view=UserHandler, endpoint='user_api', url='/users')



class LoginLogHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.LoginLogController


login_log_bp = Blueprint(name='login_logs', import_name='login_logs', url_prefix='')

easyapi.register_api(app=login_log_bp, view=LoginLogHandler, endpoint='login_log_api', url='/login_logs')