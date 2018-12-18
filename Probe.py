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
        return session().query(Probe).filter(Probe.id == id).all()

    def get_latest_probe_byid(self, id):
        session = sessionmaker(bind=engine)
        return session().query(Probe).filter(Probe.id == id).order_by(Probe.created.desc()).first()

    # FIXME - work in progress
    @property
    def nob_nd(self):
        return 1 / self.totzeit_nd

    @property
    def nob_hd(self):
        return 1 / self.totzeit_hd


    # FIXME - work in progress - sure that this is still wrong
    # better to take this as function in Record class, because Probe is almost static here?
    @property
    def get_odl_nd(self, count):
        if count > self.eigen_nd:
            diff = count - self.eigen_nd
            if count > self.nob_nd:
                count = self.nob_nd
            odl = diff / (self.empf_nd * (1.0
                                          - self.korr1_nd * count
                                          + self.korr2_nd * count ** 2
                                          - self.korr3_nd * count ** 3
                                          + self.korr4_nd * count ** 4)
                          )
        return odl

    @property
    def get_odl_hd(self, count):
        if count > self.eigen_hd:
            diff = count - self.eigen_hd
            if count > self.nob_hd:
                count = self.nob_hd
            odl = diff / (self.empf_hd * (1.0
                                          - self.korr1_hd * count
                                          + self.korr2_hd * count ** 2
                                          - self.korr3_hd * count ** 3
                                          + self.korr4_hd * count ** 4)
                          )
        return odl

    # should use weighted odl_nd and odl_hd in overlapping!!
    # ignore hd in the meanwhile
    @property
    def get_odl(self):
        odl = self.get_odl_nd
        # odl = self.get_odl_nd + self.get_odl_hd
        return odl


Base.metadata.create_all(engine, checkfirst=True)
