from DATA.TRAIN_VAL_SPLIT.train_val_split import TrainValSplit
import os

def triger():
    """
        Bu fonksiyon TrainValSplit modülünü tetikler. Daha detaylı bilgi için;
        DATA/TRAIN_VAL_SPLIT/train_val_split.py dosyasını inceleyebilirsiniz.
    """
    TrainValSplit(
        src_img_path = os.path.join("DATA", "TRAIN_VAL_SPLIT", "DATA", "IMAGES"),
        src_labels_path = os.path.join("DATA", "TRAIN_VAL_SPLIT", "DATA", "LABELS"),
        dst_train_img_path = os.path.join("DATA", "TRAIN_VAL_SPLIT", "TRAIN", "IMAGES"),
        dst_train_labels_path = os.path.join("DATA", "TRAIN_VAL_SPLIT", "TRAIN", "LABELS"),
        dst_val_img_path = os.path.join("DATA", "TRAIN_VAL_SPLIT", "VAL", "IMAGES"),
        dst_val_labels_path = os.path.join("DATA", "TRAIN_VAL_SPLIT", "VAL", "LABELS"),
        train_val_ratio = {"train":80, "val":20},
        is_label=True
    ).run()

if __name__ == "__main__":
    triger()