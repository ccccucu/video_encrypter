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

app.register_blueprint(handler.news_bp)
app.register_blueprint(handler.position_bp)
app.register_blueprint(handler.task_bp)
app.register_blueprint(handler.sender_bp)
app.register_blueprint(handler.administrator_bp)
app.register_blueprint(handler.conf_bp)
app.register_blueprint(handler.token_bp)
app.register_blueprint(handler.file_bp)
app.register_blueprint(handler.render_bp)
app.register_blueprint(handler.group_bp)
app.register_blueprint(handler.template_bp)
app.register_blueprint(handler.home_page_bp)
app.register_blueprint(handler.report_history_bp)
app.register_blueprint(handler.captcha_bp)

CORS(app, supports_credentials=True)
jwt = jwt_init()
jwt.init_app(app)
app.logger.addHandler(consoleHandler)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_logger.handlers)
    app.logger.addHandler(fileHandler)
    app.logger.setLevel(gunicorn_logger.level)
