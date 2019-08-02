from flask import Flask, Blueprint, jsonify, send_file
import easyapi
import app.core as controller
from flask_jwt import jwt_required, current_identity



class VideoHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.VideoController

video_bp = Blueprint(name='video', import_name='video', url_prefix='')

easyapi.register_api(app=video_bp, view=VideoHandler, endpoint='video_api', url='/videos')

#上传视频
@video_bp.route('/videos/upload',methods=['POST']) #不写,methods=['GET','POST'] 默认是get
def video_upload():
    try:
        pass
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
        print(video)
    except easyapi.BusinessError as e:
        return jsonify(**{
            'msg': e.err_info,
            'code': e.code,
        }), e.http_code
    return jsonify(code=200, msg='视频下载成功', data={id:id} ,video = video)
    


class WatermarkLogHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.WatermarkLogController


watermark_log_bp = Blueprint(name='watermark_logs', import_name='watermark_logs', url_prefix='')

easyapi.register_api(app=watermark_log_bp, view=WatermarkLogHandler, endpoint='watermark_log_api', url='/watermark_logs')




class DownloadLogHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.DownloadLogController


download_log_bp = Blueprint(name='download_logs', import_name='download_logs', url_prefix='')

easyapi.register_api(app=download_log_bp, view=DownloadLogHandler, endpoint='download_log_api', url='/download_logs')