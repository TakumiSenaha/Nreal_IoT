from tuning import Tuning
import flyobj
import touchsensor
import vol_and_text as voice
import DOA
import numpy as np
import usb.core
import usb.util
import pygame
import time
import RPi.GPIO as GPIO

## 全画面黒
def main_loop():
    v = voice.Voice(device_index=0)
    flyobj.init()
    while True:
        touchsensor.initial_process()
        while True:
            touch = touchsensor.read_touchsensor()
            if(touch == 1):
                break
        dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
        if dev:
            Mic_tuning = Tuning(dev)
            while(flyobj.display_thread.is_alive()):
                dB = v.get_dB()
                if(dB >= -50):
                    flyobj.gen_triangle(angle=180 - Mic_tuning.direction, scale=(dB+50)/20)
                touch = touchsensor.read_touchsensor()
                if(touch == 1):
                    ##長押し間隔の設定
                    time.sleep(0.5)
                    ##ここでもう一度touchsensor.read_touchsensor()を呼び出し
                    touch = touchsensor.read_touchsensor()
                    if(touch == 1):
                        v.change_lang()
                        time.sleep(3.0)
                        continue
                    ## 0.5秒間以上長押しされたら言語変更
                    ##turn off object generation
                    break
                time.sleep(0.1)

if __name__ == '__main__':
    try:
        main_loop()
        pass
    except KeyboardInterrupt:
        pass
    pass
GPIO.cleanup()
