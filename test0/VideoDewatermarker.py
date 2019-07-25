import os
import imp
import argparse
import shutil
import moviepy.editor as mp
import ConfigurationUtils as configurationUtil

workplace = "/test"
message_prefix = "WatermarkMessage"
config = {}


def apply_dewatermarking():
    video = mp.VideoFileClip(config.video)


    msg = config.watermarking_algorithm.extract_message_from_video(video, config)
    print msg
    return msg


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', default='output.mp4',help='Full path of video to dewatermark')
    parser.add_argument('--password',default= 'dontstealmyvideo ',  help='Password for recovering message')
    parser.add_argument('--watermark_algorithm', default='SingleFrameRandomLocation' ,  help='Algorithm to use for watermarking')
    parser.add_argument('--workplace', default=workplace,  help='Workplace for the library')
    return parser.parse_args()


def init():
    global config
    config = get_arguments()
    if os.path.isdir(config.workplace):
        shutil.rmtree(config.workplace)
    os.mkdir(config.workplace)

    config.message_prefix = message_prefix
    configurationUtil.set_watermark_algorithm(config)


def destroy():
    try:
        shutil.rmtree(config.workplace)
    except:
        print ""


if __name__ == '__main__':
    try:
        init()
        msg = apply_dewatermarking()

    finally:
        destroy()