import argparse
import ConfigurationUtils as configurationUtils
from shutil import copyfile
import os
import distutils.util

workplace = "/test"
config = {}


def apply_distortion():
    copyfile(config.video, config.output)
    temp_file_name = os.path.split(config.output)[0] + "tmp_" + os.path.split(config.output)[1]
    for distortion_algorithm in config.distortion_algorithms:
        distortion_algorithm.distort(config.output, temp_file_name, config)
        copyfile(temp_file_name, config.output)
        os.remove(temp_file_name)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video',  default='input2.mp4', help='Full path of video to distort')
    parser.add_argument('--distortion_algorithms', default='CropEdges', help='Distortion Algorithms separated with comma')
    parser.add_argument('--output',  default='output_CropEdges.mp4' ,help='Full path of output video')
    parser.add_argument('--workplace', default=workplace,  help='Workplace for the library')
    parser.add_argument('--verbose', type=distutils.util.strtobool, default='false',  help='Log the outputs')
    return parser.parse_args()


def init():
    global config
    config = get_arguments()
    configurationUtils.set_distortion_algorithms(config)


if __name__ == '__main__':
    init()
    apply_distortion()