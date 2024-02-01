from DATA.DATA_AUGMENTATION.data_augmentation import DataAugmentation

def triger():
    DataAugmentation(
        default_images_path="DATA\\DATA_AUGMENTATION\\DEFAULT_IMAGES",
        default_labels_path="DATA\\DATA_AUGMENTATION\\DEFAULT_LABELS",
        augmented_images_path="DATA\\DATA_AUGMENTATION\\AUGMENTED_IMAGES",
        augmented_labels_path="DATA\\DATA_AUGMENTATION\\AUGMENTED_LABELS",
        random_choice=True,
        noise=True,
        brightness=True,
        hue=True,
        label=True
    ).process()

triger()