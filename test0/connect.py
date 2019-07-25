# coding=utf-8
import time
import os
import importlib,sys
#importlib.reload(sys)
from flask import Flask, request, redirect, url_for, render_template
import uuid
from VideoWatermarker import watermarker
from VideoDewatermarker import dewatermarker
import argparse
import shutil
import moviepy.editor as mp
import ConfigurationUtils as configurationUtil
import distutils.util
import sys

UPLOAD_FOLDER = './'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app._static_folder = UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
def root():
        if request.method == 'POST':
            message = request.form.get('string')
            #print message
            video = request.files['file']
            if video:
                video.save(os.path.join(app.config['UPLOAD_FOLDER'], 'input.mp4'))
                watermarker('input.mp4',message)

                #message_out=dewatermarker()
                #return render_template("result.html",res=message_out)

                return render_template("watermarker.html")

        else:
            result = render_template("watermarker.html")
            return result

if __name__ == "__main__":
    app.run()




