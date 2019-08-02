from flask import Flask, Blueprint
import easyapi
import app.core as controller
from flask_jwt import current_identity, jwt_required

class UserHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.UserController

    # @jwt_required()
    # def put(self, id, *args, **kwargs):
    #     return super().put(id)
    #
    # @jwt_required()
    # def delete(self, id, *args, **kwargs):
    #     return super().delete(id)
    #
    # @jwt_required()
    # def post(self, *args, **kwargs):
    #     return super().post()

user_bp = Blueprint(name='users', import_name='users', url_prefix='')

easyapi.register_api(app=user_bp, view=UserHandler, endpoint='user_api', url='/users')