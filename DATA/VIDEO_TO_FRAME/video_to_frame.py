import os
import cv2
import time
import numpy as np



class VideoToFrame:
    """
    VideoToFrame sınıfı, kullanıcıdan video dosya/dosyalarının yolunu, oluşan framelerin kaydedileceği klasörün yolunu, 
    video içerisindeki framelerin ne zaman kayıt edileceği bilgisini, kaydedilecek framelerin çözünürlüğünü ve framelerin 
    modüler bir şekilde kaydedilip kaydedilmeyeceğini bilgilerini input olarak alır. Bu bilgileri kullanarak videoları ele 
    alır ve her 5 frame'de bir belirtilen klasöre frame'i kayıt eder. Eğer MODULER=True olarak işaretlenirse her klasörde 100 
    frame olacak şekilde klasörler oluşturur ve kayıt işlemini gerçekleştirir.
    -----
    INPUT VALUES:
        VIDEO_PATH:str = Video dosyalarının bulunduğu dosya yolunu içerir.
        FRAMES_PATH:str = Framelerin kaydedileceği dosya yolunu içerir.
        INTERVAL_COUNT:int = Video içerisindeki framelerin ne zaman kayıt edileceğini içerir.
        RESOLUTION:tuple = Framelerin istenilen çözünürlük bilgilerini içerir.
        MODULER:bool = Framelerin modüler bir yapıda kaydedilip kaydedilmeyeceği bilgisini içerir.
    -----
    OUTPUT VALUES:
        None
        Karşılaşılan hatalar error.log isminde ki dosyaya kaydedilir. Bunun dışında bu sınıf bir çıktı üretmez.
    """
    media_dir = "DATA\\VIDEO_TO_FRAME"
    def __init__(self, video_path:str=f"{media_dir}\\VIDEOS", frames_path:str=f"{media_dir}\\FRAMES", interval_count:int=5, resolution:tuple=(1280,720), moduler:bool=False):
        self.VIDEO_PATH = video_path
        self.FRAMES_PATH = frames_path
        self.INTERVAL_COUNT = interval_count
        self.RESOLUTION = resolution
        self.MODULER = moduler
        
        self.sayac = 1
        self.frame_name = 1
        self.moduler_folder_name = 1
    
    def controlVideoPath(self):
        """
            Bu fonksiyon, video dosyalarının bulunduğu klasörün yolunun doğru verilip verilmediğini kontrol eder.
        """
        video_path_status = 1
        try:
            if os.path.exists(self.VIDEO_PATH):
                video_path_status = 1
            else:
                video_path_status = 0
        except Exception as e:
            print("Hata!\nHata için error.log dosyasını kontrol ediniz.")
        return video_path_status
    
    def controlFramesPath(self):
        """
            Bu fonksiyon, framelerin kaydedileceği klasörün yolunun doğru verilip verilmediğini kontrol eder.
        """
        frames_path_status = 1
        try:
            if os.path.exists(self.FRAMES_PATH):
                frames_path_status = 1
            else:
                frames_path_status = 0
        except Exception as e:
            print("Hata!\nHata için error.log dosyasını kontrol ediniz.")
        return frames_path_status
    
    def controlIntervalCount(self):
        """
            Bu fonksiyon, video'da hangi aralıklarla framelerin kaydedileceği bilgisini taşıyan self.INTERVAL_COUNT
            değişkeninin doğru verilip verilmediğini kontrol eder.
        """
        interval_count_status = 1
        try:
            if self.INTERVAL_COUNT == int(self.INTERVAL_COUNT):
                interval_count_status = 1
            else:
                interval_count_status = 0
        except Exception as e:
            print("Hata!\nHata için error.log dosyasını kontrol ediniz.")
        return interval_count_status
    
    def controlModulerFolderCount(self):
        """
            Bu fonksiyon, MODULER=True parametresi verildiği taktirde kaydedilen frameleri sayar. Eğer bir klasör
            içerisindeki frame sayısı 100'e eşitse yeni bir klasör oluşturur ve sonraki frameleri yeni klasöre
            kaydedilmesini sağlar.
        """
        moduler_folder_status = 1
        folder_name = f"{self.FRAMES_PATH}\\{self.moduler_folder_name}"
        try:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            else:
                listdir = os.listdir(folder_name)
                if len(listdir) == 100:
                    self.moduler_folder_name += 1
                    folder_name = f"{self.FRAMES_PATH}\\{self.moduler_folder_name}"
                    os.makedirs(folder_name)
            moduler_folder_status = 1
        except Exception as e:
            moduler_folder_status = 0
            print("Hata!\nHata için error.log dosyasını kontrol ediniz.")
        return moduler_folder_status
    
    def setTheResolution(self, img:np.ndarray):
        """
            Bu fonksiyon, kullanıcının verdiği self.RESOLUTION parametresini kullanarak
            frame'in çözünürlüğünü ayarlar.
        """
        resolution_func_status = 1
        try:
            if self.RESOLUTION is not None:
                img = cv2.resize(src=img, dsize=self.RESOLUTION)
            else:
                pass
        except Exception as e:
            resolution_func_status = 0
        
        return resolution_func_status, img
            
    
    def process(self, img:np.ndarray, sayac:int):
        """
            Bu fonksiyon, self.MODULER ve self.INTERVAL_COUNT parametrelerine istinaden framelerin
            kayıt işlemini gerçekleştirir.
        """
        if not self.MODULER:
            save_frame_path = f"{self.FRAMES_PATH}\\{self.frame_name}.jpg"
        else:
            save_frame_path = f"{self.FRAMES_PATH}\\{self.moduler_folder_name}\\{self.frame_name}.jpg"

        if sayac % self.INTERVAL_COUNT == 0:
            try:
                _, img = self.setTheResolution(img=img)
            except Exception as e:
                message = f"[{time.asctime()}]: VideoToFrame modulu setTheResolution fonksiyonunda hata! Hata:{e}\n"
                with open(file="LOG\\error.log", mode="a") as file:
                    file.write(message)
                print("Hata!\nHata için error.log dosyasını kontrol ediniz.")
            try:
                cv2.imwrite(filename=save_frame_path, img=img)
                self.frame_name += 1
            except Exception as e:
                exit()
            
    def run(self):
        """
            Bu fonksiyon, VideoToFrame modülünde ki tüm fonksiyonları hata ayıklamadan geçirir ve tetikler.
            Eğer bir fonksiyonda hata alınıyorsa bu hatayı error.log dosyasına kayıt eder.
        """
        video_path_status = self.controlVideoPath()
        if video_path_status == 1:
            pass
        else:
            message = f"[{time.asctime()}]: VideoToFrame modulu controlVideoPath fonksiyonunda hata! Lutfen videolarin bulundugu dosya yolunu dogru girdiginizden emin olun.\n"
            with open(file="LOG\\error.log", mode="a") as file:
                file.write(message)
        
        frames_path_status = self.controlFramesPath()
        if frames_path_status == 1:
            pass
        else:
            message = f"[{time.asctime()}]: VideoToFrame modulu controlFramesPath fonksiyonunda hata! Lutfen frame dosyalarinin yuklenecegi yolu dogru girdiginizden emin olun.\n"
            with open(file="LOG\\error.log", mode="a") as file:
                file.write(message)
                
        interval_count_status = self.controlIntervalCount()
        if interval_count_status == 1:
            pass
        else:
            message = f"[{time.asctime()}]: VideoToFrame modulu controlIntervalCount fonksiyonunda hata! Lutfen self.INTERVAL_COUNT değişkeninin integer deger oldugundan emin olun.\n"
            with open(file="LOG\\error.log", mode="a") as file:
                file.write(message)
        
        
        
        if self.MODULER:
            listdir = os.listdir(path=self.VIDEO_PATH)
            for element in listdir:
                video_name = element
                video_path = f"{self.VIDEO_PATH}\\{video_name}"
                cap = cv2.VideoCapture(video_path)
                while cap.isOpened():
                    retval, frame = cap.read()
                    self.controlModulerFolderCount()
                    self.process(img=frame, sayac=self.sayac)
                    self.sayac += 1
            
                    
        elif not self.MODULER:
            listdir = os.listdir(path=self.VIDEO_PATH)
            for element in listdir:
                video_name = element
                video_path = f"{self.VIDEO_PATH}\\{video_name}"
                cap = cv2.VideoCapture(video_path)
                while cap.isOpened():
                    retval, frame = cap.read()
                    self.process(img=frame, sayac=self.sayac)
                    self.sayac += 1
        
        cap.release()
    

