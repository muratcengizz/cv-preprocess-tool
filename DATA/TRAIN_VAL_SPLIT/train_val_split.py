import os
import time
import cv2
import shutil
import numpy as np

class TrainValSplit:
    def __init__(self, 
                 src_img_path:str=os.path.join("DATA", "TRAIN_VAL_SPLIT", "DATA", "IMAGES"),
                 src_labels_path:str=os.path.join("DATA", "TRAIN_VAL_SPLIT", "DATA", "LABELS"),
                 dst_train_img_path:str=os.path.join("DATA", "TRAIN_VAL_SPLIT", "TRAIN", "IMAGES"),
                 dst_train_labels_path:str=os.path.join("DATA", "TRAIN_VAL_SPLIT", "TRAIN", "LABELS"), 
                 dst_val_img_path:str=os.path.join("DATA", "TRAIN_VAL_SPLIT", "VAL", "IMAGES"),
                 dst_val_labels_path:str=os.path.join("DATA", "TRAIN_VAL_SPLIT", "VAL", "LABELS"),
                 train_val_ratio:dict={"train":80, "val":20},
                 is_label:bool=False):
        """
            INPUT VALUES:
                - src_img_path: kaynak görsellerin bulunduğu dizin.
                - src_labels_path: kaynak etiketlerin bulunduğu dizin.
                - dst_train_img_path: Hedef eğitim görsellerinin kaydedileceği dizin.
                - dst_train_labels_path: Hedef eğitim etiketlerinin kaydedileceği dizin.
                - dst_val_img_path: Hedef Validasyon görsellerinin kaydedileceği dizin.
                - dst_val_labels_path: Hedef validasyon etiketlerinin kaydedileceği dizin.
                - train_val_ratio: Eğitim ve validasyon verilerinin yüzdelik oranı.
                - is_label: Eğitim ve validasyon olarak ayrıştırılacak görsellerin etiketleri varsa True olarak işaretlenir.
                etiketler de otomatik olarak ayrıştırılır.
            
            Hızlı kullanım için dosya düzeni otomatik olarak oluşturulmuştur.
        """
        self.src_img_path = src_img_path
        self.src_labels_path = src_labels_path
        self.dst_train_img_path = dst_train_img_path
        self.dst_train_labels_path = dst_train_labels_path
        self.dst_val_img_path = dst_val_img_path
        self.dst_val_labels_path = dst_val_labels_path
        self.train_val_ratio = train_val_ratio
        self.is_label = is_label
        
        self.train_key, self.train_value, self.val_key, self.val_value = "", "", 0, 0
        self.error_log_file_path = "LOG\\error.log"

    def controlSourceImagePath(self):
        """
            Bu fonksiyon, kullanıcı tarafından parametre olarak verilen kaynak görsellerin dosya yolunun doğru olup olmadığını kontrol eder.
            
        """
        source_image_path_status = 1
        if os.path.exists(path=self.src_img_path):
            source_image_path_status = 1
        else:
            source_image_path_status = 0
        return source_image_path_status
    
    def controlSourceLabelsPath(self):
        """
            Bu fonksiyon, kullanıcı tarafından parametre olarak verilen kaynak etiketlerin dosya yollarının doğru olup olmadığını kontrol eder.
        """
        source_labels_path_status = 1
        if os.path.exists(path=self.src_labels_path):
            source_labels_path_status = 1
        else:
            source_labels_path_status = 0
        return source_labels_path_status
    
    def controlDestinationTrainImagesPath(self):
        """
            Bu fonksiyon, kullanıcı tarafından parametre olarak verilen hedef eğitim görsellerinin bulunduğu dosya yolunun doğru olup olmadığını kontrol eder.
        """
        destination_train_images_status = 1
        if os.path.exists(path=self.dst_train_img_path):
            destination_train_images_status = 1
        else:
            destination_train_images_status = 0
        return destination_train_images_status
    
    def controlDestinationTrainLabelsPath(self):
        """
            Bu fonksiyon, kullanıcı tarafından parametre olarak verilen hedef eğitim etiketlerinin dosya yolunun doğru olup olmadığını kontrol eder.
        """
        destination_train_labels_status = 1
        if os.path.exists(path=self.dst_train_labels_path):
            destination_train_labels_status = 1
        else:
            destination_train_labels_status = 0
        return destination_train_labels_status
    
    def controlDestinationValidationImagesPath(self):
        """
            Bu fonksiyon, kullanıcı tarafından parametre olarak verilen hedef validasyon görsellerinin dosya yolunun doğru olup olmadığını kontrol eder.
        """
        destination_validation_images_status = 1
        if os.path.exists(path=self.dst_val_img_path):
            destination_validation_images_status = 1
        else:
            destination_validation_images_status = 0
        return destination_validation_images_status
    
    def controlDestinationValidationLabelsPath(self):
        """
            Bu fonksiyon, kullanıcı tarafından verilen hedef validasyon etiketlerinin dosya yolunun doğru olup olmadığını kontrol eder.
        """
        destination_validation_labels_status = 1
        if os.path.exists(path=self.dst_val_labels_path):
            destination_validation_labels_status = 1
        else:
            destination_validation_labels_status = 0
        return destination_validation_labels_status
    
    def controlTrainValRatio(self):
        """
            Bu fonksiyon, kullanıcın sözlük yapısında verdiği veriyi ayrıştırır. Sözlük içerisinde verilen
            verilerin doğru verilip verilmediğini kontrol eder. Train ve validation parametrelerini hafızada tutar.
            ----
            INPUT VALUES
            - None
            OUTPUT VALUES
            - [0, 1] değerlerinden birisini döner. Bu değerler fonksiyonun patlayıp patlamadığını belirtir.
            0: Fonksiyon patladı. 
            1: Fonksiyon düzgün çalışıyor.
        """
        train_val_ratio_status = 1
        train_key = list(self.train_val_ratio.keys())[0]
        train_value = list(self.train_val_ratio.values())[0]
            
        val_key = list(self.train_val_ratio.keys())[1]
        val_value = list(self.train_val_ratio.values())[1]
            
        if train_key == "train" and val_key == "val" and int(train_value) + int(val_value) == 100:
            train_val_ratio_status = 1
            self.train_key = train_key
            self.train_value = train_value
            self.val_key = val_key
            self.val_value = val_value
        else:
            train_val_ratio_status = 0
        return train_val_ratio_status
    
    def calculateTheTrainValRatio(self, train_ratio, val_ratio):
        """
            Bu fonksiyon, veri setinde ki eğitim ve validasyon verilerinin sayılarını hesaplar. 
            INPUT VALUES:
                - train_ratio: Eğitim verilerinin oranını içerir.
                - val_ratio: Validasyon verilerinin oranını içerir.
            OUTPUT VALUES:
                - Eğitim verilerinin sayısını döndürür.
        """
        listdir = os.listdir(path=self.src_img_path)
        train_ratio = round(number=(train_ratio * 0.01), ndigits=2)
        val_ratio = round(number=(val_ratio * 0.01), ndigits=2)
        count_of_train_images = int(len(listdir) * train_ratio)
        #count_of_val_images = int(len(listdir) - count_of_train_images)
        return count_of_train_images
    
    def saveDatas(self, count_of_train_images:int):
        """
            Bu fonksiyon, kaynak klasörlerden aldığı görüntü ve etiketleri hedef dizinlere train-val oranına göre gönderir.
            INPUT VALUES:
                - count_of_train_images: Eğitim görsellerinin sayısını içerir.
            OUTPUT VALUES:
                - None
        """
        listdir_src_images = os.listdir(path=self.src_img_path)
        for element in listdir_src_images:
            image_path = f"{self.src_img_path}\\{element}"
            image_name = element.split(".")[0]
            image = cv2.imread(filename=image_path)
              
            if listdir_src_images.index(element)+1 <= count_of_train_images:
                save_train_image_path = f"{self.dst_train_img_path}\\{element}"
                cv2.imwrite(filename=save_train_image_path, img=image)
            elif listdir_src_images.index(element)+1 > count_of_train_images:
                save_val_image_path = f"{self.dst_val_img_path}\\{element}"
                cv2.imwrite(filename=save_val_image_path, img=image)
        
        if self.is_label:
            listdir_src_labels = os.listdir(path=self.src_labels_path)
            for element in listdir_src_labels:
                try:
                    if listdir_src_labels.index(element)+1 <= count_of_train_images:
                        src_label_path = f"{self.src_labels_path}\\{element}"
                        dst_label_path = f"{self.dst_train_labels_path}\\{element}"
                        shutil.move(src=src_label_path, dst=dst_label_path)
                    elif listdir_src_labels.index(element)+1 > count_of_train_images:
                        src_label_path = f"{self.src_labels_path}\\{element}"
                        dst_label_path = f"{self.dst_val_labels_path}\\{element}"
                        shutil.move(src=src_label_path, dst=dst_label_path)
                except Exception as e:
                    #error_time = self.getTime()
                    error_message = f"[]: TrainValSplit modulu saveDatas() fonksiyonunda hata! Hata mesajı: {e}\n"
                    with open(file=self.error_log_file_path, mode="a", encoding="utf-8") as file:
                        file.write(error_message)
                    print("Bir hata ile karşılaşıldı. Hatayı incelemek için lütfen LOG\error.log dosyasını ziyaret ediniz.")
                    exit()
    
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
    
    def run(self):
        """
            Bu fonksiyon, tüm süreci tek bir çatı altında toplar. Hata ayıklamaları yapar. Programın düzgün çalıştığından emin olur. Tüm sistemi tetikler.
            Olası hataları error.log dosyasına kayıt eder. Kullanıcıya hata ile ilgili detaylı bilgi verir.
            INPUT VALUES:
                - None
            OUTPUT VALUES:
                - None
        """
        source_image_path_status = self.controlSourceImagePath()
        if source_image_path_status == 1:
            pass
        else:
            message_time = self.getTime()
            error_message = f"[{message_time}]: TrainValSplit modulu controlSourceImagePath() fonksiyonunda hata! Hata Mesajı: src_image_path parametresini doğru verdiğinizden emin olunuz.\n"
            with open(file=self.error_log_file_path, mode="a", encoding="utf-8") as file:
                file.write(error_message)
            print("Bir hata ile karşılaşıldı. Hatayı incelemek için lütfen LOG\error.log dosyasını ziyaret ediniz.")
            exit()

        
        source_labels_path_status = self.controlSourceLabelsPath()
        if source_labels_path_status == 1:
            pass
        else:
            message_time = self.getTime()
            error_message = f"[{message_time}]: TrainValSplit modulu controlSourceLabelsPath() fonksiyonunda hata! Hata Mesajı: src_labels_path parametresini doğru verdiğinizden emin olunuz.\n"
            with open(file=self.error_log_file_path, mode="a", encoding="utf-8") as file:
                file.write(error_message)
            print("Bir hata ile karşılaşıldı. Hatayı incelemek için lütfen LOG\error.log dosyasını ziyaret ediniz.")
            exit()
        
        dst_train_images_path_status = self.controlDestinationTrainImagesPath()
        if dst_train_images_path_status == 1:
            pass
        else:
            message_time = self.getTime()
            error_message = f"[{message_time}]: TrainValSplit modulu controlDestinationTrainImagesPath() fonksiyonunda hata! Hata Mesajı: dst_train_images_path parametresini doğru verdiğinizden emin olunuz.\n"
            with open(file=self.error_log_file_path, mode="a", encoding="utf-8") as file:
                file.write(error_message)
            print("Bir hata ile karşılaşıldı. Hatayı incelemek için lütfen LOG\error.log dosyasını ziyaret ediniz.")
            exit()
        
        dst_train_labels_path_status = self.controlDestinationTrainLabelsPath()
        if dst_train_labels_path_status == 1:
            pass
        else:
            message_time = self.getTime()
            error_message = f"[{message_time}]: TrainValSplit modulu controlDestinationTrainLabelsPath() fonksiyonunda hata! Hata Mesajı: dst_train_labels_path parametresini doğru verdiğinizden emin olunuz.\n"
            with open(file=self.error_log_file_path, mode="a", encoding="utf-8") as file:
                file.write(error_message)
            print("Bir hata ile karşılaşıldı. Hatayı incelemek için lütfen LOG\error.log dosyasını ziyaret ediniz.")
            exit()
        
        dst_val_images_path_status = self.controlDestinationValidationImagesPath()
        if dst_val_images_path_status == 1:
            pass
        else:
            message_time = self.getTime()
            error_message = f"[{message_time}]: TrainValSplit modulu controlDestinationValidationImagesPath() fonksiyonunda hata! Hata Mesajı: dst_val_images_path parametresini doğru verdiğinizden emin olunuz.\n"
            with open(file=self.error_log_file_path, mode="a", encoding="utf-8") as file:
                file.write(error_message)
            print("Bir hata ile karşılaşıldı. Hatayı incelemek için lütfen LOG\error.log dosyasını ziyaret ediniz.")
            exit()
        
        dst_val_labels_path_status = self.controlDestinationValidationLabelsPath()
        if dst_val_labels_path_status == 1:
            pass
        else:
            message_time = self.getTime()
            error_message = f"[{message_time}]: TrainValSplit modulu controlDestinationValidationLabelsPath() fonksiyonunda hata! Hata Mesajı: dst_val_labels_path parametresini doğru verdiğinizden emin olunuz.\n"
            with open(file=self.error_log_file_path, mode="a", encoding="utf-8") as file:
                file.write(error_message)
            print("Bir hata ile karşılaşıldı. Hatayı incelemek için lütfen LOG\error.log dosyasını ziyaret ediniz.")
            exit()

        control_train_val_split_status = self.controlTrainValRatio()
        if control_train_val_split_status == 1:
            pass
        else:
            message_time = self.getTime()
            error_message = f"[{message_time}]: TrainValSplit modulu controlTrainValRatio() fonksiyonunda hata! Hata Mesajı: train_val_ratio parametresini doğru verdiğinizden emin olunuz.\n"
            with open(file=self.error_log_file_path, mode="a", encoding="utf-8") as file:
                file.write(error_message)
            print("Bir hata ile karşılaşıldı. Hatayı incelemek için lütfen LOG\error.log dosyasını ziyaret ediniz.")
            exit()
        
        try:
            count_of_train_images = self.calculateTheTrainValRatio(train_ratio=self.train_value, val_ratio=self.val_value)
        except Exception as e:
            message_time = self.getTime()
            error_message = f"[{message_time}]: TrainValSplit modulu calculateTheTrainValRatio() fonksiyonunda hata! Hata Mesajı: {e}\n"
            with open(file=self.error_log_file_path, mode="a", encoding="utf-8") as file:
                file.write(error_message)
            print("Bir hata ile karşılaşıldı. Hatayı incelemek için lütfen LOG\error.log dosyasını ziyaret ediniz.")
            exit()
            
        try:
            self.saveDatas(count_of_train_images=count_of_train_images)
        except Exception as e:
            message_time = self.getTime()
            error_message = f"[{message_time}]: TrainValSplit modulu saveDatas() fonksiyonunda hata: Hata Mesajı: {e}\n"
            with open(file=self.error_log_file_path, mode="a", encoding="utf-8") as file:
                file.write(error_message)
            print("Bir hata ile karşılaşıldı. Hatayı incelemek için lütfen LOG\error.log dosyasını ziyaret ediniz.")
            exit()