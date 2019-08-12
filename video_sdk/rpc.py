from flask import Flask, request, jsonify, send_file
from flask_jsonrpc import JSONRPC
from flask_cors import CORS

import os

from water_mark import *

import aes

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/rpc')
CORS(app)



@jsonrpc.method('EnWaterMakerByPath')
def en_water_mark_by_path(path,conent, outpath):
    """
    加水印
    :param path: 输入路径
    :param conent: 水印内容
    :param outpath: 输出路径
    :return: 是否成功
    """
    msg = 'bjfu' + conent
    secret = ''
    for i in range(len(msg)):
        s = bin(ord(msg[i])).replace('0b', '')
        if (len(s) == 6):
            s = '00' + s
        if (len(s) == 7):
            s = '0' + s
        secret += s
    message = list(map(int, secret))

    workplace=os.path.dirname(path)
    apply_watermarking(path, message, outpath)
    wavNameNew = workplace+'/audio'
    strcmd = "ffmpeg -i " + path + " -f wav " + wavNameNew + ".m4a" + " -y"
    subprocess.call(strcmd, shell=True)
    file_temp =workplace+ '/temp.mp4'
    file_264=workplace+ '/H_264.mp4'
    strcmd1="ffmpeg -i "+ file_temp+" -vcodec h264 " + file_264
    subprocess.call(strcmd1, shell=True)   
    wavNameNew1 = workplace + '/audio.m4a'
    strcmd2 = "ffmpeg -i " + file_264 + " -i " + wavNameNew1 + " -c:v copy -c:a aac -strict experimental " + outpath
    subprocess.call(strcmd2, shell=True)
    return True


@jsonrpc.method('DnWaterMakerByPath')
def de_water_mark_by_path(path):
    """
    解水印
    :param path: 输入路径
    :return: 水印内容
    """
    video = VideoFileClip(path)
    msg = extract_message_from_video(path,video)
    print(msg)
    return msg

@jsonrpc.method('EnFileByPath')
def en_file_by_path(path, key, outpath):
    """
    加密
    :param path:
    :param outpath:
    :return:
    """
    return aes.aes_encrypt_by_path(path, key, outpath)


@jsonrpc.method('DeFileByPath')
def de_file_by_path(path, key, outpath):
    """
    解密
    :param path:
    :param key: 秘钥
    :param outpath:
    :return:
    """
    return aes.aes_encrypt_by_path(path, key, outpath)

@jsonrpc.method('GetThumbnailByPath')
def get_thumbnail_by_path(path, outpath):
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
