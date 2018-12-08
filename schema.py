# -*- coding: utf-8 -*-

from sqlalchemy import (Table, Column, Integer, Boolean, Float, String, DateTime, MetaData)
from db import get_dbengine

engine = get_dbengine()

meta = MetaData()
records = Table(
    'records',
    meta,
    Column('id', Integer, primary_key=True),
    Column('deviceid', String),
    Column('lowdose', Integer),
    Column('highdose', Integer),
    Column('echo', Integer),
    Column('coincidence', Boolean),
    Column('highvoltage', Boolean),
    Column('temperature', Float),
    Column('origstring', String),
    Column('created', DateTime),
)
records.create(engine, checkfirst=True)
