# -*- coding: utf-8 -*-

from sqlalchemy import (create_engine, Table, Column, Integer, Boolean, Float, String, TIMESTAMP, MetaData)

engine = create_engine("sqlite:///records.sqlite")
meta = MetaData()
records = Table(
    'records',
    meta,
    Column('id', Integer, primary_key=True),
    Column('lowdose', Integer),
    Column('highdose', Integer),
    Column('echo', Integer),
    Column('coincidence', Boolean),
    Column('highvoltage', Boolean),
    Column('temperature', Float),
    Column('origstring', String),
    Column('created', TIMESTAMP),
)
records.create(engine, checkfirst=True)