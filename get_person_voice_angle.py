from time import sleep

import usb
import usb.core
import usb.util
import struct

dev = usb.core.find(idVendor=0x2886,idProduct=0x0018)
TIMEOUT = 100000

# PARAMETERS for sound localization
PARAMETERS = {
    'DOAANGLE': (21, 0, 'int', 359, 0, 'ro', 'DOA angle. Current value. Orientation depends on build configuration.'),
    'SPEECHDETECTED': (19, 22, 'int', 1, 0, 'ro', 'Speech detection status.', '0 = false (no speech detected)',
                       '1 = true (speech detected)'),
    }

def read(param_name):
    try:
        data = PARAMETERS[param_name]
    except KeyError:
        return

    id = data[0]

    cmd = 0x80 | data[1]
    if data[2] == 'int':
        cmd |= 0x40

    length = 8

    response = dev.ctrl_transfer(
        usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
        0, cmd, id, length, TIMEOUT)

    response = struct.unpack(b'ii', response.tobytes())

    if data[2] == 'int':
        result = response[0]
    else:
        result = response[0] * (2. ** response[1])

    return result

# Find angular
if dev:

    while True:
        if read('SPEECHDETECTED') == 1:
            print(read('DOAANGLE'))
            sleep(1)