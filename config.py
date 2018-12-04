# -*- coding: utf-8 -*-

import time
import datetime
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
    time.sleep(60)
    print(datetime.datetime.now())
    ser.write(b'D')
    line1 = ser.readline()
    line2 = ser.readline()
    line3 = ser.readline()
    print(line1, line2, line3)
    if (line1 == line2 == line3):
        try:
            myrecord = Record(line1)
            for key in myrecord.data.keys():
                print(key, myrecord.data[key])
        except:
            print("An error occured.")
    else:
        print("lines differ!")
        continue

