from __future__ import absolute_import
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx


class CropEdges:


    @staticmethod
    def distort(video_input, video_output, config):
        crop_size = 120

        clip = VideoFileClip(video_input)
        clip = clip.fx(vfx.crop, x1=crop_size, y1= crop_size)
        clip.write_videofile(video_output, codec='png',  progress_bar=True, verbose=config.verbose)



