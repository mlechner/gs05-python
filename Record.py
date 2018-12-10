# -*- coding: utf-8 -*-

from sqlalchemy import (Column, Integer, Boolean, Float, String, DateTime)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from db import get_dbengine
engine = get_dbengine()

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    deviceid = Column(String)
    lowdose = Column(Integer)
    highdose = Column(Integer)
    echo = Column(Integer)
    coincidence = Column(Boolean)
    highvoltage = Column(Boolean)
    temperature = Column(Float)
    origstring = Column(String)
    created = Column(DateTime)

    def __repr__(self):
        return "%(id)s:%(ld)s|%(hd)s|%(echo)s" % ({"id": self.deviceid, "ld": self.lowdose, "hd": self.highdose, "echjo": self.echo})

    def set_data_from_recordstring(self, recordstring=""):
        split_string = recordstring.split(" ")
        split_data = {}
        for val in split_string:
            k, v = val.split(":")
            split_data[k] = v
        bittemp = split_data["T"][0], split_data["T"][1:3], split_data["T"][3:5], split_data["T"][5:]
        self.origstring = recordstring
        self.lowdose = int(split_data["N"], 16)
        self.highdose = int(split_data["H"], 16)
        self.echo = int(split_data["E"], 16)
        self.coincidence = bool(int(split_data["K"]))
        self.highvoltage = bool(int(split_data["S"]))
        self.temperature = float(str(bittemp[0]) + str(int(bittemp[1], 16)) + '.' + str((int(bittemp[2], 16)*100)/256))


Base.metadata.create_all(engine, checkfirst=True)