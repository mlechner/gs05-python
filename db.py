# -*- coding: utf-8 -*-

from Config import Config
from sqlalchemy import create_engine

def get_dbengine():
    dbconfig=Config().get_config()['db']
    if dbconfig['driver'] == 'sqlite':
        engine = create_engine(dbconfig['sqlite'])
    elif dbconfig['driver'] == 'postgresql':
        engine = create_engine('postgresql://' + dbconfig['user'] + ':'
                             + dbconfig['pass'] + '@' + dbconfig['host']
                             + '/' + dbconfig['database'])
    # use local sqlite as fallback
    else:
        engine = create_engine('sqlite:///gs05.sqlite')
    return engine

