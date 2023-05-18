'''
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

# read digital touch sensor
touchstatus = False
touchstatus_now = False
touchstatus_prev = False
touch_time_start = 0
pres_time = 0
touch_time_end = 0
def read_touchsensor():
    global touchstatus
    global touchstatus_now
    global touchstatus_prev
    global touch_time_start
    global pres_time
    global touch_time_end
    if (GPIO.input(touch) == True):
        if(not touchstatus_prev):
            touch_time_start = time.time()
        touchstatus_now = True
        touchstatus_prev = touchstatus_now
        time.sleep(0.1)
        #return ("hold")
    else:
        if (touchstatus_prev == True):
            touchstatus_now = False
            touchstatus_prev = touchstatus_now
            touch_time_end = time.time()
            pres_time = touch_time_end - touch_time_start
            if (pres_time > 0 and pres_time < 0.5):
                return (0)
            elif (pres_time >= 0.5 and pres_time < 2.5):
                return (1)
            else :
                return (2)
            pres_time = 0
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

