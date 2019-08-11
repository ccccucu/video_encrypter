import os

from flask import Flask, Blueprint
import easyapi
import app.handler as handler
from flask_cors import CORS
from app.config import Config
from app.core.auth import jwt_init
from app.utils.logger import consoleHandler, fileHandler
import logging

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'),
            static_folder=os.path.join(os.getcwd(), 'static'))
app.config.from_object(Config)

app.register_blueprint(handler.user_bp)
app.register_blueprint(handler.login_log_bp)


app.register_blueprint(handler.organization_bp)
app.register_blueprint(handler.distribut_video_bp)

app.register_blueprint(handler.video_bp)
app.register_blueprint(handler.watermark_log_bp)
app.register_blueprint(handler.download_log_bp)
app.register_blueprint(handler.token_bp)

CORS(app, supports_credentials=True)
jwt = jwt_init()
jwt.init_app(app)
app.logger.addHandler(consoleHandler)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_logger.handlers)
    app.logger.addHandler(fileHandler)
    app.logger.setLevel(gunicorn_logger.level)
