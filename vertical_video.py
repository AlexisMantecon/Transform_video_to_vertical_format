from moviepy.editor import *
from skimage.filters import gaussian


class vertical_video:
    def __init__(self):
        pass

    def blur(self, image):
        """ Returns a blurred (radius=N pixels) version of the image """
        return gaussian(image.astype(float), sigma=5)

    def get_vertical_format(self, input_video_path,
                            output_video_path,
                            codec="h264_nvenc",
                            bitrate="15000k",
                            banner_text="",
                            display_webcam=False,
                            logo_path=r"D:\Archivos\ElEmeTv\ImagenesSinFondo\El_EME_TV_SinFondo.png"):
        """
        Use example:

        from vertical_video import vertical_video

        vert_video = vertical_video()
        vert_video.get_vertical_format(input_video_path=r'C:\myvideo.mp4',
                                        output_video_path=r'C:\vf_myvideo.mp4',
                                        banner_text="Subscribe",
                                        display_webcam=True,
                                        logo_path=r"D:\logo.png"
                                        )
        """

        clip = VideoFileClip(input_video_path)

        # Get width and height of the original clip
        w, h = clip.size

        # Get a cropped gameplay with zoom for vertical format
        margen = 0.225
        x1, y1, x2, y2 = (w * margen, 1, w*(1-margen), h)
        gameplay = vfx.crop(clip, x1, y1, x2, y2)

        # Get a blurred background of the cropped gameplay
        margen_y = 0.2
        gameplay_blurred = vfx.crop(clip,
                                    x_center=w*0.5,
                                    width=w/3,
                                    y1=h*margen_y, y2=h*(1-margen_y)
                                    )
        gameplay_blurred = gameplay_blurred.fl_image(self.blur)
        gameplay_blurred = gameplay_blurred.resize(newsize=(h, w))

        # Get the cropped video of webcam
        margen_webcam = 0.25
        webcam = vfx.crop(clip, x_center=w*0.135, y_center=h *
                          0.85, width=w*margen_webcam, height=h*margen_webcam)
        webcam = webcam.margin(1, color=(136, 53, 175))
        webcam_width = abs(gameplay.size[0]-clip.size[0])
        webcam = webcam.resize(width=webcam_width)

        if display_webcam:
            logo = (ImageClip(logo_path)
                    .set_duration(clip.duration)
                    .resize(height=0.35*webcam.size[1])
                    .set_pos(("left", "top")))
            webcam_final = CompositeVideoClip([webcam, logo])
        else:
            logo = (ImageClip(logo_path)
                    .set_duration(clip.duration)
                    .resize(height=webcam.size[1])
                    .set_pos(("center", "top")))
            webcam_final = logo

        # Title for the webcam
        txt_clip = TextClip(banner_text,
                            font='Western Bang Bang Normal',
                            fontsize=100,
                            color="white",
                            stroke_color="purple",
                            stroke_width=0.5)
        txt_clip = txt_clip.set_pos(
            ("center", webcam.size[1] + 25)).set_duration(clip.duration)

        # Setting the position of the final webcam or logo
        # center de webcam
        x_webcam_pos = (gameplay.size[0]/2 -
                        webcam_final.size[0]/2) / gameplay.size[0]
        y_webcam_pos = 0.05
        webcam_final = webcam_final.set_position(
            (x_webcam_pos, y_webcam_pos), relative=True)

        # Setting the position of the gameplay
        y_gameplay_pos = (
            webcam_final.size[1]/gameplay_blurred.size[1]) + y_webcam_pos
        gameplay = gameplay.set_position(
            ("center", y_gameplay_pos), relative=True)

        # Generating the final result
        gameplay_final = CompositeVideoClip(
            [gameplay_blurred, gameplay, webcam_final, txt_clip], size=(h, w), use_bgclip=True)

        gameplay_final.write_videofile(output_video_path,
                                       codec=codec,
                                       bitrate=bitrate,
                                       threads=6)
