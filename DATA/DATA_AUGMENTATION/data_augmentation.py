import os
import cv2
import time
import shutil
import numpy as np


class DataAugmentation:
    def __init__(self, 
                 default_images_path:str=None, 
                 default_labels_path:str=None, 
                 augmented_images_path:str=None, 
                 augmented_labels_path:str=None,
                 random_choice:bool=None,
                 noise:bool=None,
                 brightness:bool=None,
                 hue:bool=None,
                 label:bool=None):
        self.DEFAULT_IMAGES_PATH = default_images_path
        self.DEFAULT_LABELS_PATH = default_labels_path
        self.AUGMENTED_IMAGES_PATH = augmented_images_path
        self.AUGMENTED_LABELS_PATH = augmented_labels_path
        self.RANDOM_CHOICE = random_choice
        self.NOISE = noise
        self.BRIGHTNESS = brightness
        self.HUE = hue
        self.LABEL = label
        
        self.error_log_file = "LOG\\error.log"
        self.sayac = 0
    
    def controlDefaultImagesPath(self):
        default_images_path_status = 1
        if os.path.exists(path=self.DEFAULT_IMAGES_PATH):
            pass
        else:
            default_images_path_status = 0
        return default_images_path_status
    
    def controlDefaultLabelsPath(self):
        default_labels_path_status = 1
        if os.path.exists(path=self.DEFAULT_LABELS_PATH):
            pass
        else:
            default_labels_path_status = 0
        return default_labels_path_status
    
    def controlAugmentedImagesPath(self):
        augmented_images_path_status = 1
        if os.path.exists(path=self.AUGMENTED_IMAGES_PATH):
            pass
        else:
            augmented_images_path_status = 0
        return augmented_images_path_status
    
    def controlAugmentedLabelsPath(self):
        augmented_labels_path_status = 1
        if os.path.exists(path=self.AUGMENTED_LABELS_PATH):
            pass
        else:
            augmented_labels_path_status = 0
        return augmented_labels_path_status
    
    def getTime(self):
        """
            Bu fonksiyon %d:%m:%y %h:%m:%s formatında anlık zamanı çıktı olarak döner.
            INPUT VALUES:
                - None
            OUTPUT VALUES:
                - time
        """
        import time
        current_time = time.localtime()
        year = current_time.tm_year
        month = current_time.tm_mon
        day = current_time.tm_mday
        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec
        message_time = f"{day:02d}:{month:02d}:{year} {hour:02d}:{minute:02d}:{second:02d}"
        return message_time
    
    def apply_noise(self, image, std:int=25):
        noise = np.random.normal(0, std, image.shape)
        noisy_image = np.clip(image + noise, 0, 255)
        return noisy_image.astype(np.uint8)
    
    def apply_brightness(self, image):
        hsv_image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2HSV)
        hsv_image[:,:,2] = np.clip(hsv_image[:,:,2] + 15 * 255, 0, 255)
        brightness_image = cv2.cvtColor(src=hsv_image, code=cv2.COLOR_HSV2BGR)
        return brightness_image
 
    def apply_hue(self, image):
        hsv_image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2HSV)
        hsv_image[:,:, 0] = (hsv_image[:,:,0] + 35) % 180
        adjust_image = cv2.cvtColor(src=hsv_image, code=cv2.COLOR_HSV2BGR)
        return adjust_image
    
    def randomChoice(self):
        def calculate(bool_list:list=None):
            for element in bool_list:
                if element == True:
                    self.sayac += 1
        calculate(bool_list=[self.BRIGHTNESS, self.HUE, self.NOISE])
        random_number = np.random.randint(low=1, high=self.sayac+1)
        choice = np.random.choice(a=["noise", "brightness", "hist_equ"], size=random_number, replace=True)
        return choice
    
    def augmentation(self):
        def label_name(image_name:str=None):
            label = image_name.split(".")[0]
            name = f"{label}.txt"
            return name
        
        listdir = os.listdir(path=self.DEFAULT_IMAGES_PATH)
        for image in listdir:
            image_path = f"{self.DEFAULT_IMAGES_PATH}\\{image}"
            label_path = label_name(image_name=image)
            full_label_path = f"{self.DEFAULT_LABELS_PATH}\\{label_path}"
            np_image = cv2.imread(filename=image_path)
            
            save_image_path = f"{self.AUGMENTED_IMAGES_PATH}\\{image}"
            save_label_path = f"{self.AUGMENTED_LABELS_PATH}\\{label_path}"
            
            if self.RANDOM_CHOICE:
                choices = self.randomChoice()
                for element in choices:
                    if element == "noise":
                        np_image = self.apply_noise(image=np_image)
                    if element == "brightness":
                        np_image = self.apply_brightness(image=np_image)
                    if element == "hist_equ":
                        np_image = self.apply_hue(image=np_image)
                cv2.imwrite(filename=save_image_path, img=np_image)
                if self.LABEL:
                    shutil.move(src=full_label_path, dst=save_label_path)
            else:
                if self.NOISE:
                    np_image = self.apply_noise(image=np_image)
                if self.BRIGHTNESS:
                    np_image = self.apply_brightness(image=np_image)
                if self.HUE:
                    np_image = self.apply_hue(image=np_image)
                cv2.imwrite(filename=save_image_path, img=np_image)
                if self.LABEL:
                    shutil.move(src=full_label_path, dst=save_label_path)
    
    def process(self):
        default_images_path_status = self.controlDefaultImagesPath()
        if default_images_path_status == 1:
            pass
        else:
            now = self.getTime()
            message = f"[{now}]: DataAugmentation modülü controlDefaultImagesPath fonksiyonunda hata! Lütfen dosya yolunu doğru verdiğinizden emin olun.\n"
            with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                file.write(message)
            print("Bir hata ile karşılaşıldı. Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
            exit()
        
        default_labels_path_status = self.controlDefaultLabelsPath()
        if default_labels_path_status == 1:
            pass
        else:
            now = self.getTime()
            message = f"[{now}]: DataAugmentation modülü controlDefaultLabelsPath fonksiyonunda hata! Lütfen dosya yolunu doğru verdiğinizden emin olun.\n"
            with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                file.write(message)
            print("Bir hata ile karşılaşıldı. Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
            exit()
            
        augmented_images_path_status = self.controlAugmentedImagesPath()
        if augmented_images_path_status == 1:
            pass
        else:
            now = self.getTime()
            message = f"[{now}]: DataAugmentation modülü controlAugmentedImagesPath fonksiyonunda hata! Lütfen dosya yolunu doğru verdiğinizden emin olun.\n"
            with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                file.write(message)
            print("Bir hata ile karşılaşıldı. Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
            exit()
            
        augmented_labels_path_status = self.controlAugmentedLabelsPath()
        if augmented_labels_path_status == 1:
            pass
        else:
            now = self.getTime()
            message = f"[{now}]: DataAugmentation modülü controlAugmentedLabelsPath fonksiyonunda hata! Lütfen dosya yolunu doğru verdiğinizden emin olun.\n"
            with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                file.write(message)
            print("Bir hata ile karşılaşıldı. Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
            exit()
            
        try:
            self.randomChoice()
        except Exception as e:
            now = self.getTime()
            message = f"[{now}]: DataAugmentation modülü randomChoice fonksiyonunda hata! {e}\n"
            with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                file.write(message)
            print("Bir hata ile karşılaşıldı. Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
            exit()
            
        try:
            self.augmentation()
        except Exception as e:
            now = self.getTime()
            message = f"[{now}]: DataAugmentation modülü augmentation fonksiyonunda hata! {e}\n"
            with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                file.write(message)
            print("Bir hata ile karşılaşıldı. Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
            exit()