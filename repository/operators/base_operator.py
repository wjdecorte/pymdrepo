"""
repository.operators.base_operator.py - Contains the base operator class

@author - jwd3 (Jason DeCorte)

@copyright:   Equifax. All rights reserved.

@license:    Apache License 2.0

@contact:    jason.decorte@equifax.com

Version History:
0.2 jwd3 02/01/2017
    Migrated select to _select to reduce redundant code
    Added select_one and select_first
    Changed select and update to return dictionary instead of class instance
    Created staticmethod convert_to_dict
    Renamed StatusTableOperator to LogTableOperator
    Added new method get_max_run_id to LogTableOperator
"""
from sqlalchemy import func, cast, BigInteger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, scoped_session
from repository.connection import repo_engine
from collections import Iterable

__version__ = "0.2"
__date__ = '01/11/2017'
__updated__ = '02/06/2017'
__all__ = []


class BaseOperator(object):
    """
    Defines methods and attributes for database operations for a table
    """
    db_table_class = None  # Set in sub-classes

    def __init__(self):
        self.session = None
        self.record = None

    def __del__(self):
        self.close_session()

    def get_session(self):
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=repo_engine))
        self.session = session()

    def close_session(self):
        if self.session:
            self.session.expunge_all()
            self.session.close()

    def update(self,**kwargs):
        """
        Update existing record if pk value is included else create a new record and return pk value
        :param kwargs: columns and values to be updated
        :return: dictionary version of updated or inserted record
        """
        if not self.session:
            self.get_session()
        if 'id' in kwargs:
            try:
                # first try to update
                self.record = self.session.query(self.db_table_class).filter_by(id=kwargs['id']).one()
            except NoResultFound:
                # if record not found and id is passed in kwargs, insert new record with id value
                self.record = self.db_table_class(id=kwargs['id'])
        else:
            self.record = self.db_table_class()
        for column,value in kwargs.items():
            if column not in ['id'] and hasattr(self.record,column):
                setattr(self.record,column,value)
        self.session.add(self.record)  # todo: not necessary for updates
        self.session.commit()
        record_dict = self.convert_to_dict(self.record)
        self.close_session()
        return record_dict

    @staticmethod
    def convert_to_dict(instance):
        """
        Convert record instance to a dictionary
        :param instance: record instance
        :return: dictionary of the data in the record instance
        """
        record_dict = dict(instance.__dict__)  # create a copy so not to mangle original version
        record_dict.pop('_sa_instance_state')
        return record_dict

    def _select(self,return_type='all',**kwargs):
        """
        Generic select method
        :param return_type: all, one or first - determines which query operator to use
        :param kwargs: contains columns and values to use as filter
        :return: dictionary or list of dictionary for each record
        """
        if not self.session:
            self.get_session()
        query = self.session.query(self.db_table_class).filter_by(**kwargs)
        if return_type == 'one':
            result = query.one_or_none()
        elif return_type == 'first':
            result = query.first()
        else:
            result = query.all()
        if isinstance(result,Iterable):
            converted_result = [self.convert_to_dict(record) for record in result]
        elif result:
            converted_result = self.convert_to_dict(result)
        else:
            converted_result = None
        self.close_session()
        return converted_result

    def select(self,**kwargs):
        return self._select(return_type='all',**kwargs)

    def select_one(self,**kwargs):
        return self._select(return_type='one',**kwargs)

    def select_first(self, **kwargs):
        return self._select(return_type='first',**kwargs)


class LogTableOperator(BaseOperator):
    """
    Defines methods and attributes for database tables used to log run information
    """
    def set_status(self,pk,status):
        """
        Special method for setting only the status of an existing record
        :param pk:
        :param status:
        :return:
        """
        self.update(id=pk,status=status)

    def get_max_run_id(self,source_id, date_filter=None):
        """
        Return the max run id for a particular source, but not greater than date_filter if provided.
        :param source_id: id value for the source
        :param date_filter: date cap in the format YYYYMMDDHH24MISS
        :return: run id
        """
        if not self.session:
            self.get_session()
        max_run_id = (self.session.query(func.max(cast(self.db_table_class.run_id,BigInteger)))
                                  .filter_by(source_id=source_id))
        if date_filter:
            max_run_id = max_run_id.filter(cast(self.db_table_class.run_id,BigInteger) <= date_filter)
        result = max_run_id.scalar()
        self.close_session()
        return int(result)
