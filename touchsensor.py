#import RPi.GPIO as GPIO
import time
import os

# sensor pin define
buzzer = 14
touch = 26
relay_in1 = 13
relay_in2 = 19

# GPIO port init


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setup(relay_in1, GPIO.OUT)
    GPIO.setup(relay_in2, GPIO.OUT)
    GPIO.setup(touch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pass

# turn on buzzer


def buzzer_on():
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.2)
    pass
# turn off buzzer


def buzzer_off():
    GPIO.output(buzzer, GPIO.HIGH)
    pass

# turn on relay


def relay_on():
    # open relay channal1 ana channal2
    GPIO.output(relay_in1, GPIO.LOW)
    GPIO.output(relay_in2, GPIO.LOW)

# turn off relay


def relay_off():
    GPIO.output(relay_in1, GPIO.HIGH)
    GPIO.output(relay_in2, GPIO.HIGH)


touchstatus = False
# read digital touch sensor


def read_touchsensor():
    global touchstatus
    if (GPIO.input(touch) == True):
        touchstatus = not touchstatus
        if touchstatus:
            # ダブルタップならばここでsleepし，処理を呼び出す（lang変更）
            print('True')
            buzzer_on()
            relay_on()
            return (True)

        else:
            print('False')
            buzzer_on()
            relay_off()
            return (False)
    pass


# main loop
def main():
    init()
    buzzer_off()
    relay_off()
    print("...................................................................Ok")
    print("...................................................................Please touch")
    while True:
        read_touchsensor()


if __name__ == '__main__':
    try:
        main()
        pass
    except KeyboardInterrupt:
        pass
    pass
GPIO.cleanup()
