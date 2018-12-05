# -*- coding: utf-8 -*-

from sqlalchemy import (create_engine, Table, Column, Integer, Boolean, Float, String, DateTime, MetaData)
from Config import Config

engine = create_engine("sqlite:///records.sqlite")
pgconfig=Config().get_config()['db']
pgengine = create_engine('postgresql://' + pgconfig['user'] + ':'
                         + pgconfig['pass'] + '@' + pgconfig['host']
                         + '/' + pgconfig['database'])

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
    Column('created', DateTime),
)
records.create(engine, checkfirst=True)
records.create(pgengine)
