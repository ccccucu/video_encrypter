from flask import Flask, request, jsonify, send_file, current_app
from flask_jsonrpc import JSONRPC
from flask_cors import CORS
import time

import os
import io
from  . import screen
from .water_mark import *
from .util import  rm_if_exits
import logging

from . import aes
import traceback

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/rpc')
CORS(app)
file_handler = logging.FileHandler('flask.log')
file_handler.setLevel(logging.DEBUG)
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)
log.addHandler(file_handler)

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

    workplace =os.path.dirname(path)

    if os.path.exists(workplace )==0:
        raise Exception("读入视频路径不存在")

    apply_watermarking(path, message, outpath)
    wavNameNew = workplace +'/audio'
    strcmd =ffmepg_path+ " -i "  + path + " -f wav " + wavNameNew + ".m4a" + "  -y"
    subprocess.call(strcmd, shell=True)
    file_temp =workplace + '/temp.mp4'

    if os.path.exists(file_temp) == 0:
        raise Exception("加水印后保存视频不成功")

    wavNameNew1 = workplace + '/audio.m4a'
    if os.path.exists(wavNameNew1) == 0:
        raise Exception("从原视频中保存音频不成功")

    strcmd2 =ffmepg_path+ " -i " + file_temp + " -i " + wavNameNew1 + " -c:v copy -c:a aac -strict experimental " + outpath + " -y"
    subprocess.call(strcmd2, shell=True)

    #销毁中间过程保存的图片、视频和音频
    os.remove(file_temp)
    os.remove(wavNameNew1)
    os.remove(workplace+'/temp.jpg')
    os.remove(os.path.dirname(path)+"/keyframe_list.txt")
    for name in os.listdir(workplace):
        if  name.startswith('frame') or name.startswith('keyframe'):  
            os.remove(os.path.join(workplace, name))
    return True


@jsonrpc.method('DeWaterMakerByPath')
def de_water_mark_by_path(path):
    """
    解水印
    :param path: 输入路径
    :return: 水印内容
    """
    video = VideoFileClip(path)
    c = Dispacher(extract_message_from_video, path,video)
    c.join(30000)
    if c.isAlive():
        print("无水印")
    elif c.error:
        print(c.error[1])
    msg = c.result
    print(msg)
    for name in os.listdir(os.getcwd()):
        if  name.startswith('de_frame'):
            os.remove(os.path.join(os.getcwd(), name))
    video.close()
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

@jsonrpc.method('Ping')
def ping_server():
    """
    解密
    :param path:
    :param key: 秘钥
    :param outpath:
    :return:
    """
    return 'ok'

@jsonrpc.method('ClientReadVideo')
def client_read_video(path, key, watermark, outpath):
    """
    提取截图
    :param path:视频路径
    :param outpath:截图路径
    :return:无
    """
    (base_path, encrpty_file) = os.path.split(path)

    origin_file = 'raw_' + encrpty_file
    origin_file_path = os.path.join(base_path, origin_file)

    watermark_file = 'raw_water' + encrpty_file
    watermark_path = os.path.join(base_path, watermark_file)
    try:
        de = de_file_by_path(path=path, key=key, outpath=origin_file_path)
        en_water_mark_by_path(path=origin_file_path, content=watermark, outpath=watermark_path)
        en = en_file_by_path(path=watermark_path, key=key, outpath=outpath)
    except Exception as e:
        traceback.print_exc()
        raise e
    finally:
        time.sleep(1)
        rm_if_exits(watermark_path) # 删除明文的水印文件
        rm_if_exits(origin_file_path) # 删除原始文件
        rm_if_exits(path)
    return outpath


@jsonrpc.method('GetThumbnailByPath')
def get_thumbnail_by_path(path, outpath):
    """
    提取截图
    :param path:视频路径
    :param outpath:截图路径
    :return:无
    """
    screen.GetScreen(path, outpath)

@app.route('/read_video', methods=['GET'])
def read_file():
    path=request.args.get('path')
    key = request.args.get('key', '')
    if not path or not os.path.isabs(path):
        return jsonify(code=404, msg='没有对应的文件'), 200
    (enfile_path, encrpty_file) = os.path.split(path)
    watermark_file = 'raw_water' + encrpty_file
    watermark_path = os.path.join(enfile_path, watermark_file)
    if os.path.exists(watermark_path):
        return send_file(watermark_path, mimetype='video/mp4', conditional=True)
    else:
        de_file_by_path(path, key, watermark_path)
        buf = None
        with open(watermark_path, 'rb') as f:
            buf = io.BytesIO(f.read())
            buf.seek(0)
        return send_file(buf, mimetype='video/mp4', conditional=True)
