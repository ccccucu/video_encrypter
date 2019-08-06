from flask import Flask, request, jsonify, send_file
from flask_jsonrpc import JSONRPC
from flask_cors import CORS

import os
from  video_sdk import screen
from video_sdk.water_mark import *

from video_sdk import aes

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/rpc')
CORS(app)



@jsonrpc.method('EnWaterMakerByPath')
def en_water_mark_by_path(path, content, outpath):
    """
    加水印
    :param path: 输入路径
    :param content: 水印内容
    :param outpath: 输出路径
    :return: 是否成功
    """
    msg = 'bjfu' + content
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
    file = workplace + '/temp.mp4'
    wavNameNew1 = workplace + '/audio.m4a'
    strcmd1 = "ffmpeg -i " + file + " -i " + wavNameNew1 + " -c:v copy -c:a aac -strict experimental " + outpath + " -y"
    subprocess.call(strcmd1, shell=True)
    return True


@jsonrpc.method('DeWaterMakerByPath')
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
    return aes.aes_decrypt_by_path(path, key, outpath)

@jsonrpc.method('ClientReadVideo')
def client_read_video(path, key, watermark, outpath):
    """
    提取截图
    :param path:视频路径
    :param outpath:截图路径
    :return:无
    """
    (base_path, encrpty_file) = os.path.split(path)
    origin_file = 'raw_'+ encrpty_file
    origin_file_path = os.path.join(base_path, origin_file)

    de_file_by_path(path=path, key=key, outpath=origin_file_path)
    en_water_mark_by_path(path=origin_file_path, content=watermark, outpath=outpath)
    return origin_file_path


@jsonrpc.method('GetThumbnailByPath')
def get_thumbnail_by_path(path, outpath):
    """
    提取截图
    :param path:视频路径
    :param outpath:截图路径
    :return:无
    """
    screen.GetScreen(path, outpath)

@app.route('/rpc/read_file', methods=['GET'])
def read_file():
    path=request.args.get('path')
    if not path or not os.path.isabs(path):
        return jsonify(code=404, msg='没有对应的文件'), 200
    return send_file(path)



if __name__ == "__main__":
    app.run(port=10086)
