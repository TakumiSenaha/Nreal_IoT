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
textobj_flg = False
text = []
def set_text(a):
    if (textobj_flg == True):
        text.append(a)

def main_loop():
    global textobj_flg
    cnt = 0
    # get angle interface
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
    if dev:
        Mic_tuning = Tuning(dev)
    # get voice interface
    #v = voice.Voice(device_index=0, callback=lambda a: set_text(a), api_key = "powerful-surf-361002-52e57728fd3a.json", language="ja-JP")
    v = voice.Voice(device_index=0, callback=lambda a: set_text(a), language="ja-JP")
    flyobj.init(width=1920, height = 1080)
    time.sleep(1.0)
    while True:
        touchsensor.initial_process()
        while True:
            touch = touchsensor.read_touchsensor()
            if (touch == 1):
                flyobj.gen_text("Flyobj Mode", 180)
                break
        while (flyobj.display_thread.is_alive()):
            dB = v.get_dB()
            if (dB >= -50):
                flyobj.gen_triangle(
                    angle=180 - Mic_tuning.direction, scale=(dB+50)/20, r_start = 10)
            touch = touchsensor.read_touchsensor()
            if (touch == 1):
                textobj_flg = True
                flyobj.gen_text("Text Generation and Flyobj Mode", 180)
                # 長押し間隔の設定
                time.sleep(3.0)
                # ここでもう一度touchsensor.read_touchsensor()を呼び出し
                touch = touchsensor.read_touchsensor()
                if (touch == 1):
                    print("end")
                    os._exit(0)
                # 0.5秒間以上長押しされたら言語変更
                # turn off object generation
                break
            time.sleep(0.1)
        #fluobj + gen_text
        while (flyobj.display_thread.is_alive()):
            textobj_flg = True
            v.recognition_enable = True
            dB = v.get_dB()
            if (dB >= -50):
                flyobj.gen_triangle(
                    angle=180 - Mic_tuning.direction, scale=(dB+50)/20, r_start = 10)
                if(len(text) >= 1):
                    flyobj.gen_text(text[0], Mic_tuning.direction)
                    del text[0]
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
                    flyobj.gen_text(f"cahnge language to {v.language}", 180)
                    time.sleep(3.0)
                    touch = touchsensor.read_touchsensor()
                    if (touch == 1):
                        print("end")
                        os._exit(0)
                    continue
                # 0.5秒間以上長押しされたら言語変更
                # turn off object generation
                textobj_flg = False
                v.recognition_enable = False
                break
            time.sleep(0.1)
        time.sleep(0.1)


if __name__ == '__main__':
    try:
        main_loop()
        pass
    except KeyboardInterrupt:
        pass
    pass
GPIO.cleanup()