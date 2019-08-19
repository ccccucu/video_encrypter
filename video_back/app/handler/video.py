import os
import easyapi
from flask import Flask, Blueprint, jsonify, send_file, request, current_app
from easyapi_tools.errors import BusinessError
from flask_jwt import jwt_required, current_identity
import app.core as controller
import app.service as service
from app.config import Config


class VideoHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.VideoController


video_bp = Blueprint(name='video', import_name='video', url_prefix='')

easyapi.register_api(app=video_bp, view=VideoHandler, endpoint='video_api', url='/videos')


@video_bp.route('/videos/upload', methods=['POST'])  # 不写,methods=['GET','POST'] 默认是get
def video_upload():
    try:
        file = request.files['file']
        id = controller.VideoController.upload_video(file=file,
                                                     origin_path=Config.ORIGIN_VIDEO_UPLOAD_PATH,
                                                     encrpty_path=Config.ENCRYPT_VIDEO_PATH,
                                                     thumnail_path=Config.VIDEO_THUMBNAIL_PATH
                                                     )

    except easyapi.BusinessError as e:
        return jsonify(**{
            'msg': e.err_info,
            'code': e.code,
        }), e.http_code
    # return jsonify(code=200, msg='上传成功')
    return jsonify(**{
        'msg': '上传成功',
        'code': 200,
        'id': id
    })


@video_bp.route('/videos/download/<int:id>', methods=['GET', 'POST'])  # 不写,methods=['GET','POST'] 默认是get
def video_download(id):
    """
    :param id:
    :return:
    """
    try:
        video = controller.VideoController.get(id)
        video_uuid = video['uuid']
        return send_file(os.path.join(Config.ENCRYPT_VIDEO_PATH, video_uuid + '.mp4'))
    except easyapi.BusinessError as e:
        return jsonify(**{
            'msg': e.err_info,
            'code': e.code,
        }), e.http_code


@video_bp.route('/videos/distribute', methods=['POST'])  # 不写,methods=['GET','POST'] 默认是get
@jwt_required()
def video_distribute():
    """
    获取分发给本人的视频
    :param id:
    :return:
    """
    try:
        body = request.json
        query, pager, sorter = VideoHandler.__url_condition__.parser(body.get("_args"))
        data, total = controller.VideoController.query_distribute_videos(query=query, sorter=sorter, pager=pager,
                                                                         current_user=current_identity)
        return jsonify(**{
            'msg': "",
            'code': 200,
            'videos': data,
            'total': total
        })
    except easyapi.BusinessError as e:
        return jsonify(**{
            'msg': e.err_info,
            'code': e.code,
        }), e.http_code


class WatermarkLogHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.WatermarkLogController

    @jwt_required()
    def post(self, *args, **kwargs):
        return super().post()


watermark_log_bp = Blueprint(name='watermark_logs', import_name='watermark_logs', url_prefix='')

easyapi.register_api(app=watermark_log_bp, view=WatermarkLogHandler, endpoint='watermark_log_api',
                     url='/watermark_logs')


@watermark_log_bp.route("/watermark_logs/search")
def watermark_logs_search():
    try:
        q = request.args.get('q', '')
        water = controller.WatermarkLogController.search_watermark(None, q)
        return jsonify(**{
            'msg': "",
            'code': 200,
            'water_mark': water,
        })
    except easyapi.BusinessError as e:
        return jsonify(**{
            'msg': e.err_info,
            'code': e.code,
        }), e.http_code


class DownloadLogHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.DownloadLogController


download_log_bp = Blueprint(name='download_logs', import_name='download_logs', url_prefix='')

easyapi.register_api(app=download_log_bp, view=DownloadLogHandler, endpoint='download_log_api', url='/download_logs')
