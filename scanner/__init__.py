import RPi.GPIO as GPIO
from cv2 import *
import time
import os
import zipfile

class Scanner():
    def __init__(self):
        self.slidenum = 50
        self.gpio = 4
        self.gpio_mode = GPIO.BCM
        self.forward_delay = 1.3
        self.forward_hold = 0.15
        self.reverse_hold = 1
        self.picture_delay = 1.5
        self.cam_port = 0
        self.cam = VideoCapture(self.cam_port)
        self.cam.set(3, 4048)
        self.cam.set(4, 3040)
        self.parentdir = "images"
        self.dirprefix = "magazine_"
        self.fileprefix = "image_"
        self.foldername = ""

    def setup(self):
        GPIO.cleanup()
        GPIO.setmode(self.gpio_mode)
        GPIO.setup(self.gpio, GPIO.OUT)

    def run(self, slides, forward = True):
        for i in range(slides):
            if forward:
                self.slide_forward()
            else:
                self.slide_reverse()
            time.sleep(self.forward_delay)
            self.take_picture(i)
        with zipfile.ZipFile(self.foldername + '.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            self.zipdir(self.foldername, zipf)

    def slide_forward(self):
        GPIO.output(self.gpio, 1)
        time.sleep(self.forward_hold)
        GPIO.output(self.gpio, 0)

    def slide_reverse(self):
        GPIO.output(self.gpio, 1)
        time.sleep(self.reverse_hold)
        GPIO.output(self.gpio, 0)

    def take_picture(self, num):
        result, image = self.cam.read()
        self.foldername = self.get_folder_name()
        if result:
            filename = self.foldername + "/" + self.fileprefix + str(num) + ".png"
            print("writing image: ", filename)
            imwrite(filename, image)
        else:
            print("No image detected. Please! try again")

    def get_folder_name(self):
        if self.foldername != "":
            return self.foldername
        dirs = os.listdir(self.parentdir)
        currentdir = self.parentdir + "/" + self.dirprefix
        currentdir += str(len(dirs))
        os.mkdir(currentdir, 0o777)
        return currentdir
    
    def zipdir(self, path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file),
                    os.path.join(path, '..')))

