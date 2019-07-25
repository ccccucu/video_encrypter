import os
import argparse
import shutil
import moviepy.editor as mp
import ConfigurationUtils as configurationUtil
import distutils.util
import sys
sys.setrecursionlimit(100000)
workplace = "/test"
message_prefix = "WatermarkMessage"
config = {}
import time


def reconstruct_video(video, config, frames_dict):
    frame_duration = 1 / video.fps

    for time in frames_dict:
        image_file = frames_dict[time]
        image_clip = mp.ImageClip(image_file) \
            .set_start(time) \
            .set_duration(frame_duration)

        video = mp.CompositeVideoClip([video, image_clip], ismask=False)


    video.write_videofile(config.output, codec='png', progress_bar=True, verbose=config.verbose)



def apply_watermarking():
    video = mp.VideoFileClip(config.video)
    frames_dict = config.watermarking_algorithm.add_watermark(video, config, config.watermark_algorithm_aggressiveness)
    print "finish_watermarker"
    reconstruct_video(video, config, frames_dict)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video',  default="input1.mp4", help='Full path of video to watermark')
    parser.add_argument('--message',  default="1410.1234.4587.4562.1410.1234", help='Message to be watermarked to video')
    parser.add_argument('--password', default= 'dontstealmyvideo ',help='Password for recovering message')
    parser.add_argument('--watermark_algorithm',  default='SingleFrameRandomLocation' ,help='Algorithm to use for watermarking')
    parser.add_argument('--watermark_algorithm_aggressiveness', type=int, default= 30, help='Algorithms agressiveness between 0 - 100')
    parser.add_argument('--output',  default='output.mp4', help='Full path of output video')
    parser.add_argument('--workplace', default=workplace,  help='Workplace for the library')
    parser.add_argument('--verbose', type=distutils.util.strtobool, default='false',  help='Log the outputs')
    return parser.parse_args()


def init():
    global config
    config = get_arguments()
    if os.path.isdir(config.workplace):
        shutil.rmtree(config.workplace)
    os.mkdir(config.workplace)

    if os.path.isfile(config.output):
        os.remove(config.output)

    config.message = configurationUtil.encode(config.password, message_prefix+config.message)
    #print config.message
    configurationUtil.set_watermark_algorithm(config)


def destroy():
    try:
        shutil.rmtree(config.workplace)
    except:
        print ("")




if __name__ == '__main__':
    try:
        time_start = time.time()
        init()
        apply_watermarking()
        time_end = time.time()
        print('totally cost', time_end - time_start)
    finally:
        destroy()
