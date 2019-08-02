import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret'

    MYSQL_USER = 'root' #数据库用户名
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''   #数据库密码
    MYSQL_HOST = 'localhost'  #ip or host
    MYSQL_PORT = 3306    #数据库端口
    MYSQL_DATABASE = 'video_encrypter'  #数据库名称

    JWT_AUTH_URL_RULE = '/login'
    JWT_ALGORITHM = 'HS256'
    JWT_LEEWAY = timedelta(seconds=300)
    JWT_VERIFY_CLAIMS = ['signature', 'exp', 'nbf', 'iat']
    JWT_NOT_BEFORE_DELTA = timedelta(seconds=0)
    JWT_EXPIRATION_DELTA = timedelta(seconds=7200)
    JWT_REQUIRED_CLAIMS = ['exp', 'iat', 'nbf']
    JWT_AUTH_HEADER_PREFIX = 'bearer'


    CAPTCHA_EXPIRE = 300
