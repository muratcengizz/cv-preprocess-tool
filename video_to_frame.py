from DATA.VIDEO_TO_FRAME import video_to_frame

vtf_dir = "DATA\\VIDEO_TO_FRAME"
videos_dir = f"{vtf_dir}\\VIDEOS"
frames_dir = f"{vtf_dir}\\FRAMES"
def triger():
    """
        Bu fonksiyon, VideoToFrame modülünü tetikler. Belirtilen dosya yolunda ki 
        videoları framelere böler ve belirtilen dizine kaydeder. Detaylı bilgi için;
        DATA/VIDEO_TO_FRAME/video_to_frame.py dosyasını inceleyebilirsiniz.
    """
    video_to_frame.VideoToFrame(
        video_path=videos_dir,
        frames_path=frames_dir,
        interval_count=5,
        resolution=(1980,224),
        moduler=True
    ).run()

if __name__ == "__main__":
    triger()