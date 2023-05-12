from tuning import Tuning
import flyobj
import numpy as np
import usb.core
import usb.util
import time

def get_direction():
    
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
    if dev:
        Mic_tuning = Tuning(dev)
        flyobj.init()
        while(flyobj.display_thread.is_alive()):
            print (Mic_tuning.direction)
            flyobj.gen_triangle(angle=180 - Mic_tuning.direction, scale=np.random.random()+1.0)
            time.sleep(0.1)
            

if __name__ == "__main__":
    get_direction()
        
        
        