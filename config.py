# -*- coding: utf-8 -*-

import time
import serial

ser = serial.Serial(
    "/dev/ttyAMA0",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

while 1:
    ser.write(b'D')
    print(ser.read(256))
    time.sleep(10)
