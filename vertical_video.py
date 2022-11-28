from moviepy.editor import *
from skimage.filters import gaussian

class vertical_video:

    def blur(image):
            """ Returns a blurred (radius=N pixels) version of the image """
            return gaussian(image.astype(float), sigma=5)
    
    def get_vertical_format(input_video_path, 
                            output_video_path,
                            codec="h264_nvenc",
                            bitrate="5000k",
                            banner_text="", 
                            display_webcam=False, 
                            logo_path=r"D:\Archivos\ElEmeTv\ImagenesSinFondo\El_EME_TV_SinFondo.png"):
        """
        Use example:

        vertical_video.get_vertical_format(
                input_video_path=r"D:\SoftwareDev\Python_Projects\Video_in_vertical_format\test_video.mp4", 
                output_video_path=r"D:\SoftwareDev\Python_Projects\Video_in_vertical_format\vf_test_video.mp4", 
                banner_text="Subscribe",
                display_webcam=True,
                logo_path=r"D:\Archivos\ElEmeTv\ImagenesSinFondo\El_EME_TV_SinFondo.png"
        )
        """

        clip = VideoFileClip(input_video_path)

        # Get width and height of the original clip
        w,h = clip.size
        print(w,h)

        # Get a cropped gameplay with zoom for vertical format
        margen = 0.225
        x1,y1,x2,y2 = (w * margen,1,w*(1-margen),h)
        gameplay = vfx.crop(clip, x1, y1, x2, y2)

        # Get a blurred background of the cropped gameplay
        gameplay_blurred = gameplay.fl_image(vertical_video.blur)
        gameplay_blurred = gameplay_blurred.resize(newsize=(h,w))

        # Get the cropped video of webcam
        margen_webcam = 0.25
        webcam = vfx.crop(clip, x_center=w*0.135, y_center=h*0.85, width=w*margen_webcam, height=h*margen_webcam)
        webcam = webcam.margin(5, color=(136, 53, 175))
        webcam_width = abs(gameplay.size[0]-clip.size[0])
        webcam = webcam.resize(width=webcam_width)

        # Title for the webcam
        txt_clip = TextClip(banner_text, fontsize = 60, color = "white", stroke_color="purple", stroke_width=2)
        txt_clip = txt_clip.set_pos(("center", "bottom")).set_duration(clip.duration)

        # Logo for the webcam
        if display_webcam:
            logo = (ImageClip(logo_path)
                    .set_duration(clip.duration)
                    .resize(height=0.35*webcam.size[1])
                    .set_pos(("left","bottom")))
            webcam_final = CompositeVideoClip([webcam, txt_clip, logo])
        else:
            logo = (ImageClip(logo_path)
                    .set_duration(clip.duration)
                    .resize(height=webcam.size[1])
                    .set_pos(("center","top")))
            webcam_final = CompositeVideoClip([logo, txt_clip])

        # Setting the position of the final webcam or logo
        x_webcam_pos = (gameplay.size[0]/2 - webcam_final.size[0]/2) / gameplay.size[0] #center de webcam
        y_webcam_pos = 0.05
        webcam_final = webcam_final.set_position((x_webcam_pos,y_webcam_pos), relative=True)

        # Setting the position of the gameplay
        y_gameplay_pos = (webcam_final.size[1]/gameplay_blurred.size[1]) + y_webcam_pos
        gameplay = gameplay.set_position(("center",y_gameplay_pos), relative=True)

        # Generating the final result
        gameplay_final = CompositeVideoClip([gameplay_blurred, gameplay, webcam_final ])
        gameplay_final = gameplay_final.resize((h,w))

        gameplay_final.write_videofile(output_video_path, 
                                        codec=codec, 
                                        bitrate=bitrate, 
                                        threads=4)
