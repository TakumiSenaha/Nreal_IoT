'''
<<<<<<< HEAD
=======
ループ文になっていないバージョン
>>>>>>> 577a2c0b4a0670d8ace8454761ad1c2d9344320c
以下のように記述して使用
----
import touchsensor

touchsensor.initial_prosess()
while True:
    if (touchsensor.read_toucsensor() == single touch):
        break
<<<<<<< HEAD

=======
        
>>>>>>> 577a2c0b4a0670d8ace8454761ad1c2d9344320c
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

<<<<<<< HEAD

=======
>>>>>>> 577a2c0b4a0670d8ace8454761ad1c2d9344320c
touchstatus = False
# read digital touch sensor


def read_touchsensor():
    global touchstatus
    touchstatus = 0
    if (GPIO.input(touch) == True):
<<<<<<< HEAD
        touchstatus = 0
        # ダブルタップならばここでsleepし，処理を呼び出す（lang変更など）
        print('True')
        time.sleep(0.3)
        return (1)
=======
        # ダブルタップならばここでsleepし，処理を呼び出す（lang変更）
        touchstatus = 1
        time.sleep(0.5)
        return (touchstatus)
>>>>>>> 577a2c0b4a0670d8ace8454761ad1c2d9344320c
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
<<<<<<< HEAD
            print(read_touchsensor())
=======
            t = read_touchsensor()
            if(t != None):
                print(t)
            
>>>>>>> 577a2c0b4a0670d8ace8454761ad1c2d9344320c
        pass
    except KeyboardInterrupt:
        pass
    pass
GPIO.cleanup()
