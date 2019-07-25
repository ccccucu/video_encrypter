from __future__ import absolute_import
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx


class BlackAndWhite:

    @staticmethod
    def distort(video_input, video_output, config):
        clip = VideoFileClip(video_input)
        clip = clip.fx(vfx.blackwhite)
        clip.write_videofile(video_output, codec='png',  progress_bar=True, verbose=config.verbose)
