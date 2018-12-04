# -*- coding: utf-8 -*-

import time
import serial
from Record import Record

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
    line = ser.readline()
    print(line)
    try:
        myrecord = Record(line)
        for key in myrecord.data.keys():
            print(key, myrecord.data[key])
    except:
        print("An error occured.")

    time.sleep(10)
