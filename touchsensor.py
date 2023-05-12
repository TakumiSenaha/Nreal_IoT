'''
ループ文になっていないバージョン
以下のように記述して使用
----
import touchsensor

touchsensor.initial_prosess()
while True:
    if (touchsensor.read_toucsensor() == single touch):
        break
        
----
'''
import RPi.GPIO as GPIO
import time
import os

# sensor pin define
touch = 26

# GPIO port init


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(touch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pass

touchstatus = False
# read digital touch sensor


def read_touchsensor():
    global touchstatus
    touchstatus = 0
    if (GPIO.input(touch) == True):
        # ダブルタップならばここでsleepし，処理を呼び出す（lang変更）
        touchstatus = 1
        time.sleep(0.5)
        return (touchstatus)
    pass


# initial_process
def initial_process():
    init()
    print("...................................................................Ok")
    print("...................................................................Please touch")


if __name__ == '__main__':
    try:
        initial_process()
        while True:
            t = read_touchsensor()
            if(t != None):
                print(t)
            
        pass
    except KeyboardInterrupt:
        pass
    pass
GPIO.cleanup()
