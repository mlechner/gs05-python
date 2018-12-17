# -*- coding: utf-8 -*-

from sqlalchemy import (Column, Integer, Float, String, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
from db import get_dbengine
engine = get_dbengine()

class Probe(Base):
    __tablename__ = 'records'
    id = Column(String, primary_key=True)
    typ = Column(Integer)
    eigen_nd = Column(Integer)
    empf_nd = Column(Float)
    totzeit_nd = Column(Float)
    korr1_nd = Column(Float)
    korr2_nd = Column(Float)
    korr3_nd = Column(Float)
    korr4_nd = Column(Float)
    ueberlapp_nd = Column(Integer)
    eigen_hd = Column(Float)
    empf_hd = Column(Float)
    totzeit_hd = Column(Float)
    korr1_hd = Column(Float)
    korr2_hd = Column(Float)
    korr3_hd = Column(Float)
    korr4_hd = Column(Float)
    ueberlapp_hd = Column(Integer)
    created = Column(DateTime)

    def __repr__(self):
        return "%(id)s:%(typ)s|%(created)s" % ({"id": self.id, "typ": self.typ, "created": self.created})

    def set_probe_from_probeconf(self, probeconf):
        # FIXME
        pass

    def get_probes_byid(self, id):
        session = sessionmaker(bind=engine)
        return session().query(Probe).filter(Probe.id==id).all()

    def get_latest_probe_byid(self, id):
        session = sessionmaker(bind=engine)
        return session().query(Probe).filter(Probe.id==id).order_by(Probe.created.desc()).first()

    # FIXME - work in progress
    @property
    def nob(self):
        return 1/self.totzeit_nd

    # FIXME - work in progress - sure that this is still wrong
    def get_odl(self, count):
        if count > self.eigen_hd:
            diff = count - self.eigen_hd
            if count > self.nob:
                count = self.nob
            odl = diff / (self.empf_hd * (1.0 - self.korr1_hd * count + self.korr2_hd * count * count - self.korr3_hd * count * count * count + self.korr4_hd * count * count * count * count))
        return odl


Base.metadata.create_all(engine, checkfirst=True)