import vol_and_text as voice
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor
import sys
import touchsensor_for_malti
import flyobj
from tuning import Tuning
import usb
import os

flg_list = [False, False, False]
text = ""
# get angle interface
dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
if dev:
    Mic_tuning = Tuning(dev)
# get voice interface
v = voice.Voice(device_index=0, callback=lambda a:set_text(a), language="ja-JP")

def set_text(a):
    text = a
def read_touchsensor():
    print("start_resd")
    func_list = [put_flyobj, put_text]
    # thread = threading.Thread(target=func_list[i], daemon=True)
    cnt_lang = 0
    cnt_pres = 0
    while (True):
        touch = touchsensor_for_malti.read_touchsensor()
        if (touch == 0):
            print("short touch")
            print(cnt_pres % len(flg_list))
            flg_list[cnt_pres % len(flg_list)] = False
            cnt_pres += 1
            flg_list[cnt_pres % len(flg_list)] = True
            print(flg_list)
            time.sleep(1)
        elif (touch == 1):
            print("long touch")
            v.change_lang(cnt_lang % len(v.lang_list))
            print(f"cahnge language to {v.language}")
            cnt_lang += 1
        elif (touch == 2):
            os._exit(0)


def put_flyobj():
    dB = v.get_dB()
    if (dB >= -50):
        flyobj.gen_triangle(
            angle=180 - Mic_tuning.direction, scale=(dB+50)/20)


def put_text():
    flyobj.gen_text(text, Mic_tuning+180)

def change_lang(cnt):
    v.change_lang(cnt % len(v.lang_list))
        # change language
    print("change lang")


def main_loop():
    print("main loop start")
    while True:
        while (flg_list[1] & flyobj.display_thread.is_alive()):
            put_flyobj()
        while (flg_list[2] & flyobj.display_thread.is_alive()):
            put_flyobj()
            put_text()


try:
    flyobj.init()
    touchsensor_for_malti.init()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(read_touchsensor)
        executor.submit(main_loop)
        
    pass
except KeyboardInterrupt:
    sys.exit()
    pass

