#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("./lcd_I2C/lib/")

import time
import datetime
import serial
import lcddriver

from Record import Record
from Config import Config
from schema import records
from schema import get_dbengine

class GS05App:
    def __init__(self, *args, **kwargs):
        self.config = Config().get_config()
        self.serconf = self.config['serial']
        self.pollconf = self.config['polling']
        self.dbconf = self.config['db']
        self.lcdconf = self.config['lcd']
        self.deviceid = self.serconf['deviceid'] if 'deviceid' in self.serconf else None
        self.valueout = int(self.lcdconf['valueout']) if 'valueout' in self.lcdconf else 2
        self.timeout = int(self.lcdconf['timestamp']) if 'timestamp' in self.lcdconf and bool(self.lcdconf['timestamp']) else False
        self.ser = serial.Serial(
            self.serconf['device'],
            baudrate=int(self.serconf['baudrate']),
            bytesize=int(self.serconf['bytesize']),
            parity=self.serconf['parity'],
            stopbits=int(self.serconf['stopbits']),
            timeout=int(self.serconf['timeout'])
        )
        # on initialise lcd
        self.lcd = None
        if bool('lcd' in self.lcdconf and self.lcdconf['lcd'] and self.lcdconf['lcd'] != '0'):
            self.lcd = lcddriver.lcd()
            self.lcd.lcd_clear()
        else:
            print("no LCD found in config")

    def run(self):
        while 1:
            time.sleep(int(self.pollconf['waittime']))
            now = datetime.datetime.now()
            print(now)
            self.ser.write(self.serconf['receivekey'].encode('ascii'))
            lines = []
            for i in range(int(self.pollconf['repeat'])):
                lines.append(self.ser.readline())
            print(lines)
            # check if all lines are equal
            if (len(lines) > 0) and (lines[1:] == lines[:-1]):
                try:
                    myrecord = Record(lines[0])
                    for key in myrecord.data.keys():
                        print(key, myrecord.data[key])
                    ins = records.insert().values(
                        deviceid=self.deviceid,
                        lowdose=myrecord.data.get('lowdose'),
                        highdose=myrecord.data.get('highdose'),
                        echo=myrecord.data.get('echo'),
                        coincidence=myrecord.data.get('coincidence'),
                        highvoltage=myrecord.data.get('highvoltage'),
                        temperature=myrecord.data.get('temperature'),
                        origstring=myrecord.record_string,
                        created=now
                    )
                    conn = get_dbengine().connect()
                    conn.execute(ins)
                except:
                    print("An error occured.")
                if self.lcd:
                    try:
                        if self.timeout:
                            self.lcd.lcd_display_string(now.strftime("%d.%m.%y %H:%M"), self.timeout)
                        if self.deviceid:
                           self.lcd.lcd_display_string("%(id)s:%(ld)s|%(hd)s|%(echo)s" %({
                                "id": self.deviceid,
                                "ld": myrecord.data.get('lowdose'),
                                "hd": myrecord.data.get('highdose'),
                                "echo": myrecord.data.get('echo')}), self.valueout)
                        else:
                            self.lcd.lcd_display_string("ld %(ld)s | hd %(hd)s" %({
                                "ld": myrecord.data.get('lowdose'),
                                "hd": myrecord.data.get('highdose')}), self.valueout)
                    except:
                        print("Could not write to LCD.")
            else:
                print("lines differ or no lines fetched!")
                continue


if __name__ == "__main__":
    app = GS05App()
    app.run()
