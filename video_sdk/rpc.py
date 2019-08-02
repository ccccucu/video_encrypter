from flask import Flask, request, jsonify, send_file
from flask_jsonrpc import JSONRPC
import os

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/rpc')


@jsonrpc.method('EnWaterMakerByPath')
def en_water_mark_by_path(path,conent, outpath):
    """
    加水印
    :param path: 输入路径
    :param conent: 水印内容
    :param outpath: 输出路径
    :return: 是否成功
    """
    pass


@jsonrpc.method('DnWaterMakerByPath')
def de_water_mark_by_path(path):
    """
    解水印
    :param path: 输入路径
    :return: 水印内容
    """
    pass


@jsonrpc.method('EnFileByPath')
def en_file_by_path(path, key, outpath):
    """
    加密
    :param path:
    :param outpath:
    :return:
    """
    pass


@jsonrpc.method('DeFileByPath')
def de_file_by_path(path, key, outpath):
    """
    解密
    :param path:
    :param key: 秘钥
    :param outpath:
    :return:
    """
    pass

@jsonrpc.method('DeFileByPath')
def de_file_by_path(path, key, outpath):
    """
    解密
    :param path:
    :param key: 秘钥
    :param outpath:
    :return:
    """
    pass

@jsonrpc.method('DeFileByPath')
def de_tbumbnail_by_path(path, outpath):
    """
    解密
    :param path:
    :param outpath:
    :return:
    """
    pass

@app.route('/api/read_file', methods=['GET'])
def read_file():
    path=request.args.get('path')
    if not path or not os.path.isabs(path):
        return jsonify(code=404, msg='没有对应的文件'), 200
    return send_file(path)

if __name__ == "__main__":
    app.run(port=10086)