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
<<<<<<< HEAD
import RPi.GPIO as GPIO
=======
>>>>>>> 577a2c0b4a0670d8ace8454761ad1c2d9344320c

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
<<<<<<< HEAD
            while(flyobj.display_thread.is_alive()):
=======
            print(flyobj.display_thread.is_alive())
            while(flyobj.display_thread.is_alive()):
                #print (Mic_tuning.direction)
>>>>>>> 577a2c0b4a0670d8ace8454761ad1c2d9344320c
                dB = v.get_dB()
                if(dB >= -50):
                    flyobj.gen_triangle(angle=180 - Mic_tuning.direction, scale=(dB+50)/20)
                touch = touchsensor.read_touchsensor()
                if(touch == 1):
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
<<<<<<< HEAD

=======
>>>>>>> 577a2c0b4a0670d8ace8454761ad1c2d9344320c
