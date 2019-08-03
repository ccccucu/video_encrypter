from flask import Flask, Blueprint, jsonify, send_file, request
import easyapi
from easyapi_tools.errors import BusinessError
import app.core as controller
import app.service as service
import os
from app.config import Config
from flask_jwt import jwt_required, current_identity



class VideoHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.VideoController

video_bp = Blueprint(name='video', import_name='video', url_prefix='')

easyapi.register_api(app=video_bp, view=VideoHandler, endpoint='video_api', url='/videos')

#上传视频
@video_bp.route('/videos/upload',methods=['POST']) #不写,methods=['GET','POST'] 默认是get
def video_upload():
    try:
        upload_file_path = os.path.join('app/', Config.FILE_UPLOAD_PATH) # app/ + files/origin/
        uuid, title, original_file_size = service.upload_file(upload_file_path)
        #request.args.get('')

        controller.VideoController.insert(data={"title": title, "uuid": uuid, "original_file_size": original_file_size,\
                                                "allow_play_time": "2019-08-02 16:37:45",\
                                                "delete_admin_user_id":1,"release_time": "2019-08-02 16:37:45","release_admin_user_id":1,\
                                                "upload_admin_user_id":1, "upload_organization_id":1
                                                })

    except easyapi.BusinessError as e:
        return jsonify(**{
            'msg': e.err_info,
            'code': e.code,
        }), e.http_code
    return jsonify(code=200, msg='上传成功')

#下载视频
@video_bp.route('/videos/download/<int:id>',methods=['GET','POST']) #不写,methods=['GET','POST'] 默认是get
def video_download(id):
    try:
        video = controller.VideoController.get(id)
        video_uuid = video['uuid']
        print(video_uuid)
    except easyapi.BusinessError as e:
        return jsonify(**{
            'msg': e.err_info,
            'code': e.code,
        }), e.http_code
    # return jsonify(code=200, msg='视频下载成功', data={id:id} ,video = video)
    file_path = os.path.join(Config.FILE_UPLOAD_PATH, str(video_uuid) )   # 'files/origin/',  str(video_uuid)

    try:
        return send_file( file_path )
    except easyapi.BusinessError as e:
        return jsonify(**{
            'msg': e.err_info,
            'code': e.code,
        }), e.http_code






class WatermarkLogHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.WatermarkLogController


watermark_log_bp = Blueprint(name='watermark_logs', import_name='watermark_logs', url_prefix='')

easyapi.register_api(app=watermark_log_bp, view=WatermarkLogHandler, endpoint='watermark_log_api', url='/watermark_logs')




class DownloadLogHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.DownloadLogController


download_log_bp = Blueprint(name='download_logs', import_name='download_logs', url_prefix='')

easyapi.register_api(app=download_log_bp, view=DownloadLogHandler, endpoint='download_log_api', url='/download_logs')