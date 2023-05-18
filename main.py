from tuning import Tuning
import flyobj
import touchsensor
import vol_and_text as voice
import numpy as np
import usb.core
import usb.util
import pygame
import time
import sys
import os
import RPi.GPIO as GPIO

# 全画面黒
text = ""
def set_text(a):
    text = a
    print(text)

def main_loop():
    cnt = 0
    # get angle interface
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
    if dev:
        Mic_tuning = Tuning(dev)
    # get voice interface
    v = voice.Voice(device_index=0, callback=lambda a: flyobj.gen_text(
        a, Mic_tuning.direction), language="ja-JP")
    flyobj.init()
    while True:
        touchsensor.initial_process()
        while True:
            touch = touchsensor.read_touchsensor()
            if (touch == 1):
                break
        while (flyobj.display_thread.is_alive()):
            dB = v.get_dB()
            if (dB >= -50):
                flyobj.gen_triangle(
                    angle=180 - Mic_tuning.direction, scale=(dB+50)/20)
                #flyobj.gen_text(text, Mic_tuning.direction)
            touch = touchsensor.read_touchsensor()
            if (touch == 1):
                # 長押し間隔の設定
                time.sleep(0.5)
                # ここでもう一度touchsensor.read_touchsensor()を呼び出し
                touch = touchsensor.read_touchsensor()
                if (touch == 1):
                    cnt += 1
                    v.change_lang(cnt % len(v.lang_list))
                    print(f"cahnge language to {v.language}")
                    time.sleep(2.0)
                    touch = touchsensor.read_touchsensor()
                    if (touch == 1):
                        print("end")
                        os._exit()
                    continue
                # 0.5秒間以上長押しされたら言語変更
                # turn off object generation
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
