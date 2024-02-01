from DATA.AUTOMATIC_PREDICT.automatic_predict import AutomaticPredict


def triger():
    """
        Bu fonksiyon AutomaticPredict modülünü tetikler. Detaylı bilgi için;
        DATA/AUTOMATIC_PREDICT/automatic_predict.py dosyasını inceleyebilirsiniz.
    """
    AutomaticPredict(
        src_images_path="DATA\\AUTOMATIC_PREDICT\\INPUT_IMAGES",
        src_videos_path="DATA\\AUTOMATIC_PREDICT\\INPUT_VIDEOS",
        dst_images_path="DATA\\AUTOMATIC_PREDICT\\OUTPUT_IMAGES",
        dst_videos_path="DATA\\AUTOMATIC_PREDICT\\OUTPUT_VIDEOS",
        weights_path="DATA\\AUTOMATIC_PREDICT\\WEIGHTS",
        video=False
    ).process()

if __name__ == "__main__":
    triger()