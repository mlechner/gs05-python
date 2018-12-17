# -*- coding: utf-8 -*-

from Config import Config
from sqlalchemy import create_engine


def get_dbengine():
    dbconfig = Config().get_config()['db']
    if dbconfig['driver'] == 'postgresql':
        proto = 'postgresql://'
    elif dbconfig['driver'] == 'mysql':
        proto = 'mysql://'
    else:
        proto = 'sqlite:///'
    if dbconfig['driver'] in ('mysql', 'postgresql'):
        engine = create_engine(proto + dbconfig['user'] + ':'
                               + dbconfig['pass'] + '@' + dbconfig['host'] + ':'
                               + dbconfig['port'] + '/' + dbconfig['database'])
    elif dbconfig['driver'] == 'sqlite':
        engine = create_engine(proto + dbconfig['sqlite'])
    # use local gs05.sqlite as fallback
    else:
        engine = create_engine(proto + 'gs05.sqlite')
    return engine
