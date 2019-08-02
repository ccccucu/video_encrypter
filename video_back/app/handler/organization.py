from flask import Flask, Blueprint
import easyapi
import app.core as controller
from flask_jwt import current_identity, jwt_required

class OrganizationHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.OrganizationController


organization_bp = Blueprint(name='organizations', import_name='organizations', url_prefix='')

easyapi.register_api(app=organization_bp, view=OrganizationHandler, endpoint='organization_api', url='/organizations')




class DistributVideoHandler(easyapi.FlaskBaseHandler):
    __controller__ = controller.DistributVideoController

distribut_video_bp = Blueprint(name='distribut_videos', import_name='distribut_videos', url_prefix='')

easyapi.register_api(app=distribut_video_bp, view=OrganizationHandler, endpoint='distribut_video_api', url='/distribut_videos')