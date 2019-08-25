import os
import sys

baae_path = ''
if getattr(sys, 'frozen', False):
    baae_path = os.path.abspath(sys._MEIPASS)

ffmepg_path = 'ffmpeg'
os.environ['IMAGEIO_FFMPEG_EXE'] = ffmepg_path
os.environ['PATH'] = os.environ['PATH'] + ":" +  os.path.abspath(baae_path)
print(ffmepg_path)
from video_sdk.rpc import app
app.run(host='127.0.0.1', port=10086)