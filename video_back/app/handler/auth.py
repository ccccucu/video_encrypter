from flask import Blueprint, jsonify
import easyapi
from flask_jwt import jwt_required, current_identity
import app.core as controller

token_bp = Blueprint(name='tokens', import_name='tokens', url_prefix='')


@token_bp.route('/tokens', methods=['GET'])
@jwt_required()
def refresh_token():
    if current_identity is not None:
        try:
            token = controller.new_token(current_identity)
        except Exception as e:
            raise easyapi.BusinessError(code=500, http_code=200, err_info=str(e))
        return jsonify({"token": token.decode('utf-8'), "msg": "", 'code': 200}), 200
    raise easyapi.BusinessError(code=500, http_code=200, err_info="请先登录")


@token_bp.route('/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    if current_identity is not None:
        current_user = dict(current_identity)
        return jsonify({'current_user': current_user, 'msg': '','code': 200}), 200
    raise easyapi.BusinessError(code=500, http_code=200, err_info="请先登录")