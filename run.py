#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import datetime
import serial
from sqlalchemy.orm import sessionmaker
from db import get_dbengine
from Record import Record
from Config import Config
sys.path.append("./lcd_I2C/lib/")
import lcddriver
from lcddriver import LCD_RETURNHOME

Session = sessionmaker(bind=get_dbengine())

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
                session = Session()
                try:
                    myrecord = Record()
                    myrecord.set_data_from_recordstring(lines[0])
                    myrecord.deviceid = self.deviceid
                    myrecord.created = now
                    session.add(myrecord)
                    session.commit()
                except:
                    session.rollback()
                    print("An error occured.")
                if self.lcd:
                    try:
                        if self.timeout:
                            self.lcd.lcd_display_string((now.strftime("%d.%m.%y %H:%M")).ljust(16), self.timeout)
                            self.lcd.lcd_write(LCD_RETURNHOME)
                        if self.deviceid:
                           self.lcd.lcd_display_string(("%(id)s:%(ld)s|%(hd)s|%(echo)s" %({
                                "id": myrecord.deviceid,
                                "ld": myrecord.lowdose,
                                "hd": myrecord.highdose,
                                "echo": myrecord.echo})).ljust(16), self.valueout)
                        else:
                            self.lcd.lcd_display_string(("ld %(ld)s | hd %(hd)s" %({
                                "ld": myrecord.lowdose,
                                "hd": myrecord.highdose})).ljust(16), self.valueout)
                        self.lcd.lcd_write(LCD_RETURNHOME)
                    except:
                        print("Could not write to LCD.")
            else:
                print("lines differ or no lines fetched!")
                continue


if __name__ == "__main__":
    app = GS05App()
    app.run()
