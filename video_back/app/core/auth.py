from flask_jwt import JWT, JWTError, logger
from werkzeug.security import safe_str_cmp, check_password_hash
from app import dao, service
from werkzeug.local import LocalProxy
from sqlalchemy.exc import OperationalError, IntegrityError, DataError
from flask import request, current_app, jsonify, _request_ctx_stack
from datetime import datetime
from collections import OrderedDict
import jwt
import time

def jwt_init():
    custom_jwt = JWT()

    @custom_jwt.authentication_handler
    def authenticate(**kwargs):
        login_type = kwargs.get('type', 'admin')

        if login_type == 'admin':
            #管理员登录
            try:
                account = kwargs.get('username', None)
                password = kwargs.get('password', None)
                user = dao.UserDao.get(query={'account': account, 'role': 'admin' })
                password_hash = user['password']

                if not check_password_hash(password_hash,password):
                    raise JWTError('Bad Request', '管理员账号或密码错误')
                return dict(user)
            except (OperationalError, IntegrityError ) as e:
                raise JWTError('Bad Request', str(e))
        else:
            # 用户登录
            try:
                account = kwargs.get('username', None)
                password = kwargs.get('password', None)
                user = dao.UserDao.get(query={'account': account, 'role': 'user' })
                password_hash = user['password']

                if not check_password_hash(password_hash,password):
                    raise JWTError('Bad Request', '用户名或密码错误')
                return dict(user)
            except (OperationalError, IntegrityError ) as e:
                raise JWTError('Bad Request', str(e))


    @custom_jwt.jwt_payload_handler
    def jwt_payload(identity):
        return new_payload(identity)


    @custom_jwt.identity_handler
    def identity(payload):
        user = payload['identity']
        return user


    @custom_jwt.auth_response_handler
    def auth_response(access_token, identity):
        return jsonify({'code': 200, 'token': access_token.decode('utf-8'), 'user': dict(identity)})


    @custom_jwt.jwt_error_handler
    def jwt_error(error):
        logger.error(error)
        return jsonify(OrderedDict([
            ('code', 500),
            ('msg', error.description)
        ])), error.status_code, error.headers


    @custom_jwt.auth_request_handler
    def auth_request():
        data = request.get_json()
        _jwt = LocalProxy(lambda: current_app.extensions['jwt'])

        identity_data = _jwt.authentication_callback(**data)

        if identity_data:
            access_token = _jwt.jwt_encode_callback(identity_data)
            return _jwt.auth_response_callback(access_token, identity_data)
        else:
            raise JWTError('Bad Request', '用户或密码错误')

    return custom_jwt

# 生成token的新载荷
def new_payload(identity):
    # 这里都使用三个字母的原因是保证 JWT 的紧凑

    #（保留声明）reserved claims ，预定义的 一些声明：
    # “exp”: [expiration time] 过期时间
    # “nbf”: 表示当前时间在nbf里的时间之前，则Token不被接受
    # “iss”: [issuer] token签发者
    # “aud”: [audience] 接收者
    # “iat”: 发行时间
    # “sub”: [subject]


    #（公有声明）public claims : 这个部分可以随便定义，但是要注意和 IANA JSON Web Token 冲突
    #（私有声明）private claims : 这个部分是共享被认定信息中自定义部分。


    iat = datetime.utcnow()  # 发行时间
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')  # 过期时间 3600*24*30*12 秒
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')  # 表示当前时间在nbf里的时间之前，则Token不被接受

    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': dict(identity)}  # 有效用户信息载荷


def new_token(identity):
    secret = current_app.config['JWT_SECRET_KEY']
    algorithm = current_app.config['JWT_ALGORITHM']
    required_claims = current_app.config['JWT_REQUIRED_CLAIMS']

    payload = new_payload(identity)
    missing_claims = list(set(required_claims) - set(payload.keys()))

    if missing_claims:
        raise RuntimeError('Payload is missing required claims: %s' % ', '.join(missing_claims))

    headers = None

    return jwt.encode(payload, secret, algorithm=algorithm, headers=headers)

