import os
import cv2
import time
from ultralytics import YOLO

class AutomaticPredict:
    def __init__(self, src_images_path:str=None, src_videos_path:str=None, dst_images_path:str=None, dst_videos_path:str=None, weights_path:str=None, video:bool=None):
        self.SRC_IMAGES_PATH = src_images_path
        self.SRC_VIDEOS_PATH = src_videos_path
        self.DST_IMAGES_PATH = dst_images_path
        self.DST_VIDEOS_PATH = dst_videos_path
        self.WEIGHTS_PATH = weights_path
        self.IS_VIDEO = video
        
        self.error_log_file = "LOG\\error.log"
    
    def controlSourceImagesPath(self):
        """
            Bu fonksiyon kullanıcıdan alınan kaynak resim dosyalarının bulunduğu dosya yolunun doğru olup olmadığını kontrol eder.
            
            PARAMETRELER:
                Giriş parametresi yok.
            ÇIKTI:
                src_images_path_status -> [0, 1]: Kullanıcının doğru dosya yolu verip vermediğine dair değer döndürür.
        """
        src_images_path_status = 1
        if os.path.exists(self.SRC_IMAGES_PATH):
            pass
        else:
            src_images_path_status = 0
        return src_images_path_status
    
    def controlSourceVideosPath(self):
        """
            Bu fonksiyon kullanıcıdan alınan kaynak videoların bulunduğu dosya yolunun doğru olup olmadığını kontrol eder.
            
            PARAMETRELER:
                Giriş parametresi yok.
            ÇIKTI:
                src_videos_path_status -> [0, 1]: Kullanıcının doğru dosya yolu verip vermediğine dair değer döndürür.
        """
        src_videos_path_status = 1
        if os.path.exists(self.SRC_VIDEOS_PATH):
            pass
        else:
            src_videos_path_status = 0
        return src_videos_path_status
    
    def controlDestinationImagesPath(self):
        """
            Bu fonksiyon kullanıcının verdiği hedef resim dosyalarının kaydedileceği dosya yolunun doğru olup olmadığını kontrol eder.
            
            PARAMETRELER:
                Giriş parametresi yok.
            ÇIKTI:
                dst_images_path_status -> [0, 1]: Kullanıcının doğru dosya yolu verip vermediğine dair bir değer döndürür.
        """
        dst_images_path_status = 1
        if os.path.exists(self.DST_IMAGES_PATH):
            pass
        else:
            dst_images_path_status = 0
        return dst_images_path_status
    
    def controlDestinationVideosPath(self):
        """
            Bu fonksiyon kullanıcının verdiği hedef video dosyalarının kaydedileceği dosya yolunun doğru olup olmadığını kontrol eder.
            
            PARAMETRELER:
                Giriş parametresi yok.
            ÇIKTI:
                dst_videos_path_status -> [0, 1]: Kullanıcının doğru dosya yolu verip vermediğine dair bir değer döndürür.
        """
        dst_videos_path_status = 1
        if os.path.exists(self.DST_VIDEOS_PATH):
            pass
        else:
            dst_videos_path_status = 0
        return dst_videos_path_status
    
    def controlWeightsPath(self):
        """
            Bu fonksiyon kullanıcının verdiği ağırlık dosyasının/dosyalarının dosya yolunun doğru verilip verilmediğini kontrol eder.
            
            PARAMETRELER:
                Giriş parametresi yok.
            ÇIKTI:
                weights_path_status -> [0, 1]: Kullanıcının doğru dosya yolu verip vermediğine dair bir değer döndürür.
        """
        weights_path_status = 1
        if os.path.exists(path=self.WEIGHTS_PATH):
            pass
        else:
            weights_path_status = 0
        return weights_path_status
    
    def getTime(self):
        """
            Bu fonksiyon %d:%m:%y %h:%m:%s formatında anlık zamanı çıktı olarak döner.
            
            PARAMETRELER:
                - Giriş parametresi yok.
            ÇIKTI:
                - message_time -> [%d:%m:%y %h:%m:%s]
        """
        current_time = time.localtime()
        year = current_time.tm_year
        month = current_time.tm_mon
        day = current_time.tm_mday
        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec
        message_time = f"{day:02d}:{month:02d}:{year} {hour:02d}:{minute:02d}:{second:02d}"
        return message_time
    
    def predictionOnImages(self):
        """
            Bu fonksiyon src_images_path dosya yolundaki resim dosyaları üzerinde ağırlık dosyasını kullanarak tahmin işlemi yapar.
            Sonucu ise dst_images_path dosya yoluna kaydeder.
            
            PARAMETRELER:
                Giriş parametresi yok.
            ÇIKTI:
                Çıktı parametresi yok.
        """
        listdir = os.listdir(self.SRC_IMAGES_PATH)
        for image in listdir:
            image_path = f"{self.SRC_IMAGES_PATH}\\{image}"
            save_image_path = f"{self.DST_IMAGES_PATH}\\{image}"
            
            np_image = cv2.imread(filename=image_path)
            
            weights = os.listdir(self.WEIGHTS_PATH)
            for weight in weights:
                weight_path = f"{self.WEIGHTS_PATH}\\{weight}"
                model = YOLO(model=weight_path).predict(source=np_image)
                annotated_image = model[0].plot()
                cv2.imwrite(filename=save_image_path, img=annotated_image)
                
    def predictionOnVideos(self):
        """
            Bu fonksiyon src_videos_path dosya yolundaki video dosyaları üzerinde ağırlık dosyasını kullanarak tahmin işlemi yapar.
            Sonucu ise dst_videos_path dosya yoluna kaydeder.
            
            PARAMETRELER:
                Giriş parametresi yok.
            ÇIKTI:
                Çıktı parametresi yok.
        """
        listdir = os.listdir(path=self.SRC_VIDEOS_PATH)
        for video in listdir:
            video_path = f"{self.SRC_VIDEOS_PATH}\\{video}"
            save_video_path = f"{self.DST_VIDEOS_PATH}\\{video}"
            
            cap = cv2.VideoCapture(video_path)
            cap_fps = cap.get(propId=cv2.CAP_PROP_FPS)
            cap_height = int(cap.get(propId=cv2.CAP_PROP_FRAME_HEIGHT))
            cap_width = int(cap.get(propId=cv2.CAP_PROP_FRAME_WIDTH))
            cap_fourcc = cv2.VideoWriter_fourcc(*"DIVX")
            writer = cv2.VideoWriter(filename=save_video_path, fourcc=cap_fourcc, fps=cap_fps, frameSize=(cap_width, cap_height))
            
            weights = os.listdir(path=self.WEIGHTS_PATH)
            for weight in weights:
                weight_path = f"{self.WEIGHTS_PATH}\\{weight}"
                
                while cap.isOpened():
                    retval, frame = cap.read()
                    model = YOLO(model=weight_path).predict(source=frame)
                    annotated_frame = model[0].plot()
                    writer.write(image=annotated_frame)
                cap.release()
                writer.release()
    
    def process(self):
        """
            Bu fonksiyon tüm fonksiyonları hata ayıklamadan geçirir. Hata tespit edildiği taktirde, hata ele alınıp error.log 
            dosyasına kaydedilir. Aksi halde tahmin işlemlerini kullanıcının verdiği parametrelere göre tamamlar.
            
            PARAMETRELER:
                Giriş parametresi yok.
            ÇIKTI:
                Çıktı parametresi yok.
        """
        src_images_path_status = self.controlSourceImagesPath()
        if src_images_path_status == 1:
            pass
        else:
            now = self.getTime()
            message = f"[{now}]: AutomaticPredict modülü controlSourceImagesPath fonksiyonunda hata! Lütfen dosya yolunu doğru verdiğinizden emin olun.\n"
            with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                file.write(message)
            print("Hata ile karşılaşıldı! Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
            exit()
        
        src_videos_path_status = self.controlSourceVideosPath()
        if src_videos_path_status == 1:
            pass
        else:
            now = self.getTime()
            message = f"[{now}]: AutomaticPredict modülü controlSourceVideosPath fonksiyonunda hata! Lütfen dosya yolunu doğru verdiğinizden emin olun.\n"
            with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                file.write(message)
            print("Hata ile karşılaşıldı! Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
            exit()
            
        dst_images_path_status = self.controlDestinationImagesPath()
        if dst_images_path_status == 1:
            pass
        else:
            now = self.getTime()
            message = f"[{now}]: AutomaticPredict modülü controlDestinationImagesPath fonksiyonunda hata! Lütfen dosya yolunu doğru verdiğinizden emin olun.\n"
            with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                file.write(message)
            print("Hata ile karşılaşıldı! Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
            exit()
            
        dst_videos_path_status = self.controlDestinationVideosPath()
        if dst_videos_path_status == 1:
            pass
        else:
            now = self.getTime()
            message = f"[{now}]: AutomaticPredict modülü controlDestinationVideosPath fonksiyonunda hata! Lütfen dosya yolunu doğru verdiğinizden emin olun.\n"
            with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                file.write(message)
            print("Hata ile karşılaşıldı! Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
            exit()
            
        weights_path_status = self.controlWeightsPath()
        if weights_path_status == 1:
            pass
        else:
            now = self.getTime()
            message = f"[{now}]: AutomaticPredict modülü controlWeightsPath fonksiyonunda hata! Lütfen dosya yolunu doğru verdiğinizden emin olun.\n"
            with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                file.write(message)
            print("Hata ile karşılaşıldı! Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
            exit()
        
        if self.IS_VIDEO:
            try:
                self.predictionOnVideos()
            except Exception as e:
                now = self.getTime()
                message = f"[{now}]: AutomaticPredict modülü predictionOnVideos fonksiyonunda hata! {e}\n"
                with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                    file.write(message)
                print("Hata ile karşılaşıldı! Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
                exit()
        elif self.IS_VIDEO is not True:
            try:
                self.predictionOnImages()
            except Exception as e:
                now = self.getTime()
                message = f"[{now}]: AutomaticPredict modülü predictionOnImages fonksiyonunda hata! {e}\n"
                with open(file=self.error_log_file, mode="a", encoding="utf-8") as file:
                    file.write(message)
                print("Hata ile karşılaşıldı! Hata mesajı için lütfen LOG/error.log dosyasını inceleyiniz.")
                exit()