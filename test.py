import vol_and_text as voice
import numpy as np
import time
import threading
import sys
import touchsensor
import flyobj
from tuning import Tuning
import usb

flg_list = [False, False, False]
touchsensor.initial_process()
v = voice.Voice(device_index=0)
flyobj.init()
def read_touchsensor():
    func_list = [put_flyobj, put_text, change_lang]
    thread_list = []
    for i in range(len(func_list)):
        thread = threading.Thread(target=func_list[i], daemon=True)
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    cnt = -1
    while (True):
        touch = touchsensor.read_touchsensor()
        if (touch==1):
            print("touch")
            func_list[cnt%len(func_list)] = False
            cnt += 1
            func_list[cnt%len(func_list)] = True
            time.sleep(1)
   
def put_flyobj():
    while True:
        if (flg_list[0] == True):
            print("flyobj")
            dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
            if dev:
                Mic_tuning = Tuning(dev)
                while(flyobj.display_thread.is_alive()):
                    dB = v.get_dB()
                    if(dB >= -50):
                        flyobj.gen_triangle(angle=180 - Mic_tuning.direction, scale=(dB+50)/20)
            
            

def put_text():
    while True:
        if (flg_list[1] == True):
            #テキスト表示関数実行
            print("put text")

def change_lang():
    if (flg_list[2] == True):
        #change language
        print("change lang")


if __name__ == '__main__':
    try:
        read_touchsensor()
        pass
    except KeyboardInterrupt:
        sys.exit()
        pass
    pass
