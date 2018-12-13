#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from db import get_dbengine
from Record import Record
from Config import Config
from serial import Serial
from serial import SerialException
from Lcd import Lcd


class GS05App:
    def __init__(self, *args, **kwargs):
        self.config = Config().get_config()
        self.serialconf = self.config['serial']
        self.pollconf = self.config['polling']
        self.dbconf = self.config['db']
        self.lcdconf = self.config['lcd']
        self.deviceid = self.serialconf['deviceid'] if 'deviceid' in self.serialconf else None
        self.valueout = int(self.lcdconf['valueout']) if 'valueout' in self.lcdconf else 2
        self.timestampout = int(self.lcdconf['timestamp']) if 'timestamp' in self.lcdconf and bool(self.lcdconf['timestamp']) else False
        if bool('serial' in self.config and self.serialconf['device']):
            try:
                # FIXME
                self.serial = Serial(
                    self.serialconf['device'],
                    baudrate=int(self.serialconf['baudrate']),
                    bytesize=int(self.serialconf['bytesize']),
                    parity=self.serialconf['parity'],
                    stopbits=int(self.serialconf['stopbits']),
                    timeout=int(self.serialconf['timeout'])
                )
            except SerialException as se:
                print(se)
        else:
            self.serial = None
        self.lines = None
        self.now = datetime.datetime.now()
        # on initialise lcd
        if bool('lcd' in self.lcdconf and self.lcdconf['lcd'] and self.lcdconf['lcd'] != '0'):
            self.lcd = Lcd()
        else:
            self.lcd = None
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
                # FIXME
                print(Record.get_lowdose_threshold(180))
                if self.lcd:
                    self.lcd.display_record(record, this=self)
            else:
                print("lines differ or no lines fetched!")
            time.sleep(float(self.pollconf['waittime']) - ((time.time() - start) % float(int(self.pollconf['waittime']))))

    def ser_write(self):
        try:
            self.serial.write(self.serialconf['receivekey'].encode('ascii'))
        except SerialException as se:
            print(se)
        except AttributeError as ae:
            print(ae)

    def ser_read(self):
        self.lines = []
        try:
            for i in range(int(self.pollconf['repeat'])):
                self.lines.append(self.serial.readline())
            print(self.lines)
        except SerialException as se:
            print(se)
        except AttributeError as ae:
            print(ae)

    def check_lines(self):
        if self.lines:
            return (len(self.lines) > 0) and (self.lines[1:] == self.lines[:-1])

    def save_record(self):
        session = self.Session()
        try:
            myrecord = Record()
            myrecord.set_data_from_recordstring(self.lines[0])
            myrecord.deviceid = self.deviceid
            myrecord.created = self.now
            session.add(myrecord)
            session.commit()
            return myrecord
        except SQLAlchemyError:
            session.rollback()
            print("An error occured.")


if __name__ == "__main__":
    app = GS05App()
    app.run()
