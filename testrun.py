#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from db import get_dbengine
from Record import Record
from Probe import Probe
from Config import Config


class GS05App:
    def __init__(self, *args, **kwargs):
        self.config = Config().get_config()
        self.serialconf = self.config['serial']
        self.probeconf = self.config['probe']
        self.pollconf = self.config['polling']
        self.dbconf = self.config['db']
        self.lcdconf = self.config['lcd']
        self.deviceid = self.probeconf['id'] if 'id' in self.probeconf else None
        self.valueout = int(self.lcdconf['valueout']) if 'valueout' in self.lcdconf else 2
        self.timestampout = int(self.lcdconf['timestamp']) if 'timestamp' in self.lcdconf and bool(
            self.lcdconf['timestamp']) else False
        self.serial = None
        self.probe = Probe()
        self.probe.set_probe_from_probeconf(self.probeconf)
        self.lines = None
        self.now = datetime.datetime.now()
        self.lcd = None
        self.Session = sessionmaker(bind=get_dbengine())
        self.save_probe()

    def run(self):
        start = time.time()
        while True:
            self.now = datetime.datetime.now()
            self.test_read()
            print(self.now)
            if self.check_lines():
                record = self.save_record()
                print(self.probe.get_odl(record.lowdose))
                if self.lcd:
                    self.lcd.display_record(record, this=self)
            else:
                print("lines differ or no lines fetched!")
            time.sleep(
                float(self.pollconf['waittime']) - ((time.time() - start) % float(int(self.pollconf['waittime']))))

    def save_probe(self):
        session = self.Session()
        try:
            session.add(self.probe)
            session.commit()
        except SQLAlchemyError as se:
            session.rollback()
            print(se)

    def test_read(self):
        f = open("example/output.txt", "r")
        self.lines = []
        try:
            for i in range(int(self.pollconf['repeat'])):
                self.lines.append(f.readline())
            print(self.lines)
        except AttributeError as ae:
            print(ae)

    def check_lines(self):
        if self.lines:
            return (len(self.lines) > 0) and self.lines[0] != '' and (self.lines[1:] == self.lines[:-1])

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
