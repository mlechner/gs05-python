#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import serial
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from db import get_dbengine
from Record import Record
from Config import Config
from Lcd import Lcd
import lcd_I2C.lib.lcddriver as lcddriver


class GS05App:
    def __init__(self, *args, **kwargs):
        self.config = Config().get_config()
        self.serconf = self.config['serial']
        self.pollconf = self.config['polling']
        self.dbconf = self.config['db']
        self.lcdconf = self.config['lcd']
        self.deviceid = self.serconf['deviceid'] if 'deviceid' in self.serconf else None
        self.valueout = int(self.lcdconf['valueout']) if 'valueout' in self.lcdconf else 2
        self.timestampout = int(self.lcdconf['timestamp']) if 'timestamp' in self.lcdconf and bool(self.lcdconf['timestamp']) else False
        self.ser = serial.Serial(
            self.serconf['device'],
            baudrate=int(self.serconf['baudrate']),
            bytesize=int(self.serconf['bytesize']),
            parity=self.serconf['parity'],
            stopbits=int(self.serconf['stopbits']),
            timeout=int(self.serconf['timeout'])
        )
        self.lines = None
        self.now = datetime.datetime.now()
        # on initialise lcd
        self.lcd = None
        if bool('lcd' in self.lcdconf and self.lcdconf['lcd'] and self.lcdconf['lcd'] != '0'):
            self.lcd = Lcd()
        else:
            print("no LCD found in config")
        self.Session = sessionmaker(bind=get_dbengine())

    def run(self):
        start = time.time()
        while True:
            self.now = datetime.datetime.now()
            self.ser_write()
            self.ser_read()
            print(self.now)
            if self.check_lines():
                record = self.save_record()
                if self.lcd:
                    self.display_record(record)
                    # FIXME
                    #self.lcd.display_record(record, self)
            else:
                print("lines differ or no lines fetched!")
            time.sleep(float(self.pollconf['waittime']) - ((time.time() - start) % float(int(self.pollconf['waittime']))))

    def ser_write(self):
        self.ser.write(self.serconf['receivekey'].encode('ascii'))

    def ser_read(self):
        self.lines = []
        for i in range(int(self.pollconf['repeat'])):
            self.lines.append(self.ser.readline())
        print(self.lines)

    def check_lines(self):
        if self.lines:
            return (len(self.lines) > 0) and (self.lines[1:] == self.lines[:-1])

    def save_record(self, lines):
        session = self.Session()
        try:
            myrecord = Record()
            myrecord.set_data_from_recordstring(lines[0])
            myrecord.deviceid = self.deviceid
            myrecord.created = self.now
            session.add(myrecord)
            session.commit()
            return myrecord
        except SQLAlchemyError:
            session.rollback()
            print("An error occured.")

    # FIXME move this function to Lcd.py
    def display_record(self, record):
        try:
            if self.timestampout:
                self.lcd.lcd_display_string((self.now.strftime("%d.%m.%y %H:%M")).ljust(16), self.timestampout)
                self.lcd.lcd_write(lcddriver.LCD_RETURNHOME)
                self.lcd.lcd_write(lcddriver.LCD_BLINKOFF)
            if self.deviceid:
                self.lcd.lcd_display_string(("%(id)s:%(ld)s|%(hd)s|%(echo)s" % ({
                    "id": record.deviceid,
                    "ld": record.lowdose,
                    "hd": record.highdose,
                    "echo": record.echo})).ljust(16), self.valueout)
            else:
                self.lcd.lcd_display_string(("ld %(ld)s | hd %(hd)s" % ({
                    "ld": record.lowdose,
                    "hd": record.highdose})).ljust(16), self.valueout)
            self.lcd.lcd_write(lcddriver.LCD_RETURNHOME)
            self.lcd.lcd_write(lcddriver.LCD_BLINKOFF)
        except RuntimeError:
            print("Runtime Error: Could not write to LCD.")


if __name__ == "__main__":
    app = GS05App()
    app.run()
