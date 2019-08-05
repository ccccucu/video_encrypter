import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret'

    MYSQL_USER = 'root' #数据库用户名
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''   #数据库密码Root!!2018
    MYSQL_HOST = 'localhost'  #ip or host
    MYSQL_PORT = 3306    #数据库端口
    MYSQL_DATABASE = 'video_encrypter'  #数据库名称

    JWT_AUTH_URL_RULE = '/login'
    JWT_ALGORITHM = 'HS256'
    JWT_LEEWAY = timedelta(seconds=300)
    JWT_VERIFY_CLAIMS = ['signature', 'exp', 'nbf', 'iat']
    JWT_NOT_BEFORE_DELTA = timedelta(seconds=0)
    JWT_EXPIRATION_DELTA = timedelta(seconds=3600*24*30*12)
    JWT_REQUIRED_CLAIMS = ['exp', 'iat', 'nbf']
    JWT_AUTH_HEADER_PREFIX = 'bearer'


    # 用户登录接口已由flask-jwt默认定义好，默认路由是"/auth"，可以在配置文件中配置:
    # JWT_AUTH_URL_RULE = '/login'
    # 修改登录接口路由为'/login'
    # 需要注意的是，登录接口的传值要使用 application/json 形式


    CAPTCHA_EXPIRE = 300

    #文件路径
    FILE_UPLOAD_PATH = 'files/origin/'