import moviepy.video.io.ImageSequenceClip as ImgClip

#TODO: add method to change fps based on number of images.
def create_video_from_images(image_paths:list[str], phone_num:str, fps = 4):
    print("Preparing Video...")
    clip = ImgClip.ImageSequenceClip(image_paths,fps=fps)
    clip.write_videofile(f'{phone_num}_wrapped_{fps}.mp4')