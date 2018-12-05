# -*- coding: utf-8 -*-

import time
import datetime
import serial
from Record import Record
from Config import Config

config = Config().get_config()
serconf = config['serial']
pollconf = config['polling']
dbconf = config['db']

print("config read")

ser = serial.Serial(
    serconf['device'],
    baudrate=int(serconf['baudrate']),
    bytesize=int(serconf['bytesize']),
    parity=serconf['parity'],
    stopbits=int(serconf['stopbits']),
    timeout=int(serconf['timeout'])
)



while 1:
    time.sleep(int(pollconf['waittime']))
    print(datetime.datetime.now())
    ser.write(b'D')
    lines = []
    for i in int(pollconf['repeat']):
        lines.append(ser.readline())
    print(lines)
    if (len(lines) > 0) and (lines[1:] == lines[:-1]):
        try:
            myrecord = Record(lines[0])
            for key in myrecord.data.keys():
                print(key, myrecord.data[key])
        except:
            print("An error occured.")
    else:
        print("lines differ or no lines fetched!")
        continue

