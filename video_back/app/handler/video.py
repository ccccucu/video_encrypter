from flask import Flask, Blueprint, jsonify
import easyapi
import app.core as controller
from flask_jwt import jwt_required, current_identity

video_bp = Blueprint(name='video', import_name='video', url_prefix='')

class VideoHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.VideoController

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
    #     upload_admin_user_account = current_identity['id']
    #     return super().post(upload_admin_user_account=upload_admin_user_account)
    #
    #
    # @jwt_required()
    # def get(self,id: int, *args, **kwargs):
    #     return super().get(id)


@video_bp.route('/videos/upload')
def video_upload():
    try:
        pass
    except easyapi.BusinessError as e:
        return jsonify(**{
            'msg': e.err_info,
            'code': e.code,
        }), e.http_code
    return jsonify(code=200, msg='视频上传成功')

easyapi.register_api(app=video_bp, view=VideoHandler, endpoint='video_api', url='/videos')
