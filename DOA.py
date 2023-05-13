# not use
from tuning import Tuning
import flyobj
import numpy as np
import usb.core
import usb.util
import time

def get_direction(dB):
    
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
    if dev:
        Mic_tuning = Tuning(dev)
        flyobj.init()
        while((flyobj.display_thread.is_alive()) and (dB >= -50) ):
            #print (Mic_tuning.direction)
            flyobj.gen_triangle(angle=180 - Mic_tuning.direction, scale=(dB+50)/20)
            time.sleep(0.1)
            
if __name__ == "__main__":
    get_direction()
        
        
        