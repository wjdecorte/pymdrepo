"""
repository/connection.py - Library containing connection objects

@author - Jason DeCorte

@copyright:  2016 Equifax. All rights reserved.

@license:    Apache License 2.0

@contact:    jason.decorte@equifax.com

Version History:
0.2 jwd3 11/11/2016 Hotfix
    Added SQLA recycle parameters
0.3 jwd3 12/15/2016
    Removed dependency on Airflow
0.3.1 jwd3 02/12/2017
    Removed unused import statements
"""
from sqlalchemy import create_engine

from . import METADATA_DATABASE_URL

__version__ = "0.3"
__date__ = '2016-10-20'
__updated__ = '2016-12-15'

engine_args = {'pool_size': 5,
               'pool_recycle': 3600}

repo_engine = create_engine(METADATA_DATABASE_URL, **engine_args)
